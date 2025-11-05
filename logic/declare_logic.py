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
                row.CreatedBy = Security.current_user().id
                #    if Config.SECURITY_ENABLED == True else 'public'
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

    def test_state_change(row: models.TaskInstance, old_row: models.TaskInstance, logic_row:LogicRow):
        '''
        Only validate state change (update) if the status is changing using TaskFlow
        PEND -> NEW
        NEW -> INP
        INP -> COMP
        '''
        if logic_row.ins_upd_dlt == 'upd' and row.Status != old_row.Status:
            pass

            next_tasks = row.ToTaskTaskFlowList
            for task in next_tasks:
                if task.ToTaskId == row.TaskId and task.Condition in (None, '', '1=1', 'True'):
                    return
            pass
        return True
    
    #Rule.constraint(validate=models.TaskInstance,calling=test_state_change,error_msg="TaskInstance Status can only change forward")
    '''
    def start_workflow(logic_row: LogicRow):
        """
        Start the workflow for a New Application 
        """
        if logic_row.ins_upd_dlt != 'ins':
            return
        from api.api_discovery.workflow import _start_workflow as start_workflow_function
        process_name = "Application Workflow"
        application_id = logic_row.row.ApplicationId
        started_by = logic_row.row.StartedBy
        priority = logic_row.row.Priority
        start_workflow_function(process_name=process_name, application_id=application_id, started_by=started_by, priority=priority)
        
        
    Rule.after_flush_row_event(on_class=models.WFApplication, calling=start_workflow)

    
 
    '''
    def update_status(row: models.StageInstance, old_row: models.StageInstance , logic_row:LogicRow):
        """
        Update the status of the workflow application
        """
        if logic_row.ins_upd_dlt != 'upd':
            return
        if row.CompletedCount == row.TotalCount:
            row.status == 'Completed'
            row.completed_at = datetime.datetime.now()
        elif row.TotalCount != old_row.TotalCount and row.CompletedCount < row.TotalCount:
            row.status == 'Running'
            row.started_at = datetime.datetime.now()
    
    #Rule.row_event(on_class=models.StageInstance, calling=update_status)
    #WF Application Dashboard
    '''
    Rule.count(derive=models.StageInstance.TotalCount, as_count_of=models.TaskInstance)
    Rule.count(derive=models.StageInstance.CompletedCount, as_count_of=models.TaskInstance, where="Status" == 'Completed')
    '''

    
    def start_workflow(row: models.TaskInstance, old_row: models.TaskInstance , logic_row:LogicRow):
        """
        Start the workflow for a New Application 
        """
        if logic_row.ins_upd_dlt != 'ins':
            return
        from api.api_discovery.start_workflow import _start_workflow as start_workflow_function
        process_name = "OU Application Init"
        application_id = row.ApplicationID        
        started_by = 'system'
        priority = "HIGH"
        headers = {'Content-Type': 'application/json'}
        from flask import g
        if "access_token" in g:
            headers['Authorization'] = f'Bearer {g.access_token}'
        # Deadlocks
        #response = requests.post('http://localhost:5656/start_workflow', json={
        #    'process_name': process_name,
        #    'application_id': application_id,
        #    'started_by': started_by,
        #    'priority': priority
        #}, headers=headers)
        # calling start_workflow_function directly inside a flush event did not work
        #start_workflow_function(process_name=process_name, application_id=application_id, started_by=started_by, priority=priority) 
    
    Rule.after_flush_row_event(on_class=models.WFApplication, calling=start_workflow)
    
    def update_stages(row: models.TaskInstance, old_row: models.TaskInstance , logic_row:LogicRow):
        """
        Update the status of the workflow application
        """
        if logic_row.ins_upd_dlt != 'upd' and old_row and row.Status != old_row.Status:
            return
        stage = row.Stage
        if stage is None:
            return
        application_id = stage.ProcessInstance.ApplicationId
        application = models.WFApplication.query.filter_by(ApplicationID=application_id).one_or_none()
            
        if row.TaskDef.TaskType == 'LANESTART':
            stage.Status = 'IN_PROGRESS'
            application.StartedDate = datetime.datetime.now()
            logic_row.update(reason="update stage status to INP", row=application)
        elif row.TaskDef.TaskType == 'LANEEND' and row.Status == 'COMPLETED':
            stage.Status = 'COMPLETED'
            stage.CompletedDate = datetime.datetime.now()
            logic_row.update(reason="update stage status to COMPLETED", row=application)
        elif row.TaskDef.TaskType == 'START':
            if application is not None:
                application.Status = 'INP'
                application.StartedDate = datetime.datetime.now()
                logic_row.update(reason="update application status to INP", row=application)
        elif row.TaskDef.TaskType == 'END' and row.Status == 'COMPLETED':
            if application is not None:
                application.Status = 'WTH' if application.Status == 'WTH' else 'COMPL'
                application.CompletedDate = datetime.datetime.now()
                logic_row.update(reason=f"update application status to {application.Status}", row=application)
        
    #Rule.row_event(on_class=models.TaskInstance, calling=update_stages)


    Rule.sum(derive=models.WFQuote.TotalAmount, as_sum_of=models.WFQuoteItem.Amount, where=None)
    app_logger.debug("..logic/declare_logic.py (logic == rules + code)")

