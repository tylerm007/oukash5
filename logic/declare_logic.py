import datetime, os
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.logic_bank import Rule
import database.models as models
import api.system.opt_locking.opt_locking as opt_locking
from security.system.authorization import Grant, Security
from logic.load_verify_rules import load_verify_rules
import integration.kafka.kafka_producer as kafka_producer
import logging
from config.config import Config
from dotmap import DotMap

app_logger = logging.getLogger(__name__)

declare_logic_message = "ALERT:  *** No Rules Yet ***"  # printed in api_logic_server.py

def declare_logic():
    ''' Declarative multi-table derivations and constraints, extensible with Python.
 
    Brief background: see readme_declare_logic.md
    
    Your Code Goes Here - Use code completion (Rule.) to declare rules
    '''
    def round_decimal_amounts(row: models.WFQuoteItem, old_row: models.WFQuoteItem, logic_row: LogicRow):
        """
        Round decimal amounts to prevent ODBC precision errors.
        SQL Server DECIMAL(10,2) only supports 2 decimal places.
        """
        if hasattr(row, 'Amount') and row.Amount is not None:
            # Round to 2 decimal places to match DECIMAL(10,2) column definition
            if isinstance(row.Amount, (float, Decimal)):
                row.Amount = Decimal(str(row.Amount)).quantize(Decimal('0.01'))
                logic_row.log(f"Rounded Amount from {old_row.Amount if old_row else 'None'} to {row.Amount}")
    # Fix ODBC precision errors by rounding decimal fields
    Rule.early_row_event(models.WFQuoteItem, calling=round_decimal_amounts)
    
    if os.environ.get("WG_PROJECT"):
        # Inside WG: Load rules from docs/expprt/export.json
        load_verify_rules()
    else:
        # Outside WG: load declare_logic function
        from logic.logic_discovery.auto_discovery import discover_logic
        discover_logic()

    def handle_all(logic_row: LogicRow):  # #als: TIME / DATE STAMPING, OPTIMISTIC LOCKING
        """
        This is generic - executed for all classes.

        Invokes optimistic locking, and checks Grant permissions.

        Also provides user/date stamping.

        Args:
            logic_row (LogicRow): from LogicBank - old/new row, state
        """

        if os.getenv("APILOGICPROJECT_NO_FLASK") is not None:
            print("\ndeclare_logic.py Using TestBase\n")
            return  # enables rules to be used outside of Flask, e.g., test data loading

        if logic_row.is_updated() and logic_row.old_row is not None and logic_row.nest_level == 0:
            opt_locking.opt_lock_patch(logic_row=logic_row)

        Grant.process_updates(logic_row=logic_row)
        did_stamping = False
        enable_stamping = False # set True to enable date/user stamping
        if enable_stamping:  # #als:  DATE / USER STAMPING
            row = logic_row.row
            if logic_row.ins_upd_dlt == "ins" and hasattr(row, "CreatedDate"):
                row.CreatedDate = datetime.datetime.now()
                did_stamping = True
            if logic_row.ins_upd_dlt == "ins" and hasattr(row, "CreatedBy"):
                row.CreatedBy = Security.current_user().Username                #    if Config.SECURITY_ENABLED == True else 'public'
                did_stamping = True
            if logic_row.ins_upd_dlt == "upd" and hasattr(row, "ModifiedDate"):
                row.ModifiedDate = datetime.datetime.now()
                did_stamping = True
            if logic_row.ins_upd_dlt == "upd" and hasattr(row, "ModifiedBy"):
                row.ModifiedBy = "admin"# Security.current_user().id  \
                    #if Config.SECURITY_ENABLED == True else 'public'
                did_stamping = True
            if did_stamping:
                logic_row.log("early_row_event_all_classes - handle_all did stamping")     
    Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all)

    #als rules report
    from api.system import api_utils
    # api_utils.rules_report()


    
    def find_next_task_by_name(task_instance:models.TaskInstance, task_name:str) -> models.TaskInstance:
        # Find the next TaskInstance in the workflow by TaskName
        
        #task_instance = models.TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
        if not task_instance:
            return None
        stage_id = task_instance.StageId
        application_id = task_instance.ApplicationId
        task_def = models.TaskDefinition.query.filter_by(TaskName=task_name).first()
        if not task_def:
            app_logger.warning(f"No TaskDefinition found with TaskName {task_name}")
            return None
        next_task_instance = models.TaskInstance.query.filter_by(TaskDefinitionId=task_def.TaskId, ApplicationId=application_id).first()
        if next_task_instance:
            return next_task_instance
        return None

    def create_invoice(task_instance: models.TaskInstance, logic_row: LogicRow = None) -> bool:
        #Create an EventAction for the given TaskInstanceId and EventKey

        invoice_fee_task = find_next_task_by_name(task_instance, "Assign Invoice Amount")
        from api.api_discovery.event_action import _create_invoice_fee
        fee =  float(invoice_fee_task.Result) if invoice_fee_task else 0.0
        application_id = task_instance.ApplicationId
        application = models.WFApplication.query.filter_by(ApplicationID=application_id).first()    
        company_id = application.CompanyID
        invoice_fee = _create_invoice_fee(company_id=company_id, fee_amount=fee, logic_row=logic_row)
        if not invoice_fee:
            app_logger.error( f"Failed to create invoice fee for TaskInstanceId {task_instance.TaskInstanceId}")
            return False
        task_name = "Mark Invoice Paid"
        #task_instance = models.TaskInstance.query.filter_by(TaskInstanceId=task_instance.TaskInstanceId).first()
        next_task_instance = find_next_task_by_name(task_instance, task_name)
        # We find the next task to start an EventAction
        if next_task_instance:
            from api.api_discovery.event_action import _create_event
            event_key = f"INVOICE_{invoice_fee.INVOICE_ID}"
            _create_event(next_task_instance.TaskInstanceId, event_key=event_key, logic_row=logic_row)
            print(f'{{"EventKey": "{event_key}"}}')
            app_logger.info(f"EventAction created for TaskInstanceId {task_instance.TaskInstanceId} with EventKey {event_key}")
    
        return True
    
    def update_stages(row: models.TaskInstance, old_row: models.TaskInstance , logic_row:LogicRow):
        """
        Update the status of the workflow application
        """
        # Only process updates where status actually changed
        if logic_row.ins_upd_dlt != 'upd':
            return
        if old_row and row.Status == old_row.Status:
            return  # Status didn't change, nothing to do

        application_id = row.ApplicationId
        application = models.WFApplication.query.filter_by(ApplicationID=application_id).one_or_none()
        task_def = row.TaskDefinition
        if task_def.TaskName == 'AssignNCRC' and row.Status == 'COMPLETED':
            if application is not None:
                application.Status = 'INP'
                application.StartedDate = datetime.datetime.now()
                logic_row.update(reason="Update application status to INP", row=application)
        #elif task_def.TaskType in ('STAGESTART'):
        #    stage.Status = 'IN_PROGRESS'
        #    application.StartedDate = datetime.datetime.now()
        #    logic_row.update(reason="update stage status to INP", row=stage)
        #elif task_def.TaskType in ('STAGEEND') and row.Status == 'COMPLETED':
        #    stage.Status = 'COMPLETED'
        #    stage.CompletedDate = datetime.datetime.now()
        #    logic_row.update(reason="update stage status to COMPLETED", row=stage)
        elif task_def.TaskName == 'End Certification' and row.Status == 'COMPLETED':
            if application is not None:
                application.Status = 'WTH' if application.Status == 'WTH' else 'COMPL'
                application.CompletedDate = datetime.datetime.now()
                logic_row.update(reason=f"Update application status to {application.Status}", row=application)
        else:
            status = None
            TaskName = task_def.TaskName
            if row.Status != 'COMPLETED':
                return
            if TaskName == 'Generated Invoice and Send':
                if create_invoice(row, logic_row=logic_row):
                    status = 'PAYPEND'
            # Specific TaskDef.TaskName logic can go here if needed
            elif TaskName == 'Notify Customer': status = 'COMPL'
            elif TaskName == 'to Withdrawn Y/N' and row.Result == 'YES': status = 'WTH'
            elif TaskName == 'Withdraw Application' and row.Result == 'YES': status = 'WTH'
            elif TaskName == 'Send Contract' and row.Result == 'YES': status = 'CONTRACT' 
            elif TaskName == 'Inspection Report Submitted to IAR': status = 'REVIEW'
            elif TaskName == 'Schedule Inspection': status = 'INSPECTION'
            if status is not None:
                application.Status = status
                application.CompletedDate = datetime.datetime.now()
                logic_row.update(reason=f"Update application status to {application.Status}", row=application)
        
    Rule.commit_row_event(on_class=models.TaskInstance, calling=update_stages)
    Rule.sum(derive=models.WFQuote.TotalAmount, as_sum_of=models.WFQuoteItem.Amount, where=None)
    app_logger.debug("..logic/declare_logic.py (logic == rules + code)")

