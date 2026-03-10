import datetime, os
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.logic_bank import Rule
import database.models as models
import database.oukash_models as oukash_models
import database.submission_models as submission_models
import api.system.opt_locking.opt_locking as opt_locking
from security.system.authorization import Grant, Security
from logic.load_verify_rules import load_verify_rules
import integration.kafka.kafka_producer as kafka_producer
import logging
import json
import threading
from database.utils import parse_sqlserver_json

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

    def _create_wfapplication_background(owns_id: int, submission_id: str, headers: dict):
        '''
        Background worker to create WFApplication via API call.
        Runs in separate thread to avoid blocking main logic flow.
        '''
        from logic.logic_discovery.workflow_engine import get_client_uri, make_secure_request
        #from flask import current_app
        
        # Need Flask app context for any Flask operations
        #with current_app.app_context():
        try:
            server_uri = get_client_uri()
            
            app_logger.info(f"[BACKGROUND] Creating WFApplication for owns_id: {owns_id}, submission_id: {submission_id}")
            
            # Use secure request helper for self-signed certificates
            response = make_secure_request(
                'get', 
                f"{server_uri}/createApplication?owns_id={owns_id}&submission_id={submission_id}", 
                headers=headers, 
                verify=False
            )
            
            if response.status_code == 200:
                app_logger.info(f"[BACKGROUND] ✅ Created WFApplication - owns_id: {owns_id}, submission_id: {submission_id}. Response: {response.text}")
            else:
                app_logger.error(f"[BACKGROUND] ❌ Failed to create WFApplication - owns_id: {owns_id}, code: {response.status_code}, message: {response.text}")
                
        except Exception as e:
            app_logger.error(f"[BACKGROUND] 💥 Exception creating WFApplication for owns_id: {owns_id}: {e}")

    def create_wfapplication(row: models.WFApplication, owns_id:int, logic_row: LogicRow):
        '''
        Create a new Workflow application by calling the KASH API with the OWNS ID and ExternalAppRef.
        
        This function fires off a background thread and returns immediately (fire and forget).
        The actual API call happens asynchronously to avoid blocking the main logic flow.
        
        Args:
            row: WFApplication row
            owns_id: OWNS ID to link
            logic_row: LogicRow context
            
        Returns:
            dict: Immediate response indicating background task started
        '''
        from flask import request
        
        # Prepare headers
        headers = {
            'Content-Type': 'application/json'
        }
        if hasattr(request, 'headers'):
            # Copy authorization header if present
            if request.headers.get('Authorization'):
                headers['Authorization'] = request.headers.get('Authorization')
            elif request.headers.get('access_token'):
                headers['Authorization'] = request.headers.get('access_token')
        
        submission_id = row.ExternalAppRef
        
        # Start background thread (fire and forget)
        thread = threading.Thread(
            target=_create_wfapplication_background,
            args=(owns_id, submission_id, headers),
            daemon=True  # Daemon thread exits when main program exits
        )
        thread.start()
        
        app_logger.info(f"🚀 Started background task to create WFApplication for owns_id: {owns_id}, submission_id: {submission_id}")
        
        # Return immediately
        data = {
            'Result': True,
            'Message': f"Background task started to create WFApplication for owns_id: {owns_id}, submission_id: {submission_id}",
            'Status': 'PENDING'
        }
        return data
    

    def resolve_plant(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
        '''
        Given a TaskInstance for ResolvePlant, call the KASH API to get plant details and store in ResultData.
        1. There can be up to 5 different ResolvePlant tasks (task_def ResolvePlant1,2,3,4,5)
        2. The ResultData should include the PlantId which links to SubmissionPlant
        3. The SubmissionPlant can link to SubmissionMatch which has PLANT info
        4. if Result is empty - then we use the SubmssionPlant data to create a new PLANT_TB
        5. if Result is not empty - then we update create or find an OWNS_TB record linking comapny and plant ID

        '''
       
        result = row.Result
        ownstb = None
        company_row = get_resolve_company(row)
        # If both Company and Plant are in Result - lookup OWNS record and add OwnsId to ResultData
        if result is not None and company_row is not None:
            result_data = parse_sqlserver_json(row.ResultData) if row.ResultData and isinstance(row.ResultData, str) else {}
            plant_id = int(result) if isinstance(result, int) or (isinstance(result, str) and result.isdigit()) else None
            company_id = getattr(company_row ,'Result') if company_row else None
            ownstb = oukash_models.OWNSTB.query.filter_by(COMPANY_ID=company_id, PLANT_ID=plant_id).first()
        else:
            pass
            plant = oukash_models.PLANTTB(
                NAME=f"Plant for {row.ApplicationId}",
            ) #TODO
            # We do not have a plant match - we need to create and add to OWNS_TB and link to company and plant in ResultData for downstream tasks to use   
        owns_id = None
        if ownstb:
            owns_id = getattr(ownstb,'ID')
            result_data["OWNSID"] = owns_id
        else:
            owns = oukash_models.OWNSTB()
            setattr(owns, 'COMPANY_ID', int(company_id))
            setattr(owns, 'PLANT_ID', int(plant_id))
            setattr(owns, 'START_DATE', datetime.datetime.now())
            setattr(owns, 'Status', 'PENDING')
            setattr(owns, 'ACTIVE', 1)
            
            try:
                logic_row.session.add(owns)
                logic_row.insert(reason="Create OWNS record", row=owns)
                owns_id = owns.ID
                result_data["OWNSID"] = owns_id
                row.ResultData = json.dumps(result_data)
                logic_row.log(f"Created OWNS record with ID {owns_id} for company_id: {company_id} and plant_id: {plant_id}")
            except Exception as e:
                app_logger.error(f"Error creating OWNS record: {e}")
                return

    def get_resolve_company(row: models.TaskInstance):
        # Helper function to get the related ResolveCompany task result for the same application
        application_id = row.ApplicationId
        task_instances = models.TaskInstance.query.filter_by(ApplicationId=application_id).all()
        for task_instance in task_instances:
            task_def = task_instance.TaskDefinition
            if task_def.TaskName.startswith('ResolveCompany'):
                return task_instance
        return None
    
    def resolve_company(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
        '''
        Given a TaskInstance for ResolveCompany, call the KASH API to get company details and store in ResultData.
        '''
        result = row.Result
        if result is not None:
            company_id = int(result) if isinstance(result, int) or (isinstance(result, str) and result.isdigit()) else None
            if company_id:
                # Call KASH API to get company details and store in ResultData
                company = oukash_models.COMPANYTB.query.filter_by(COMPANY_ID=company_id).first()
                if company:
                    company_details = {
                        "CompanyId": company.COMPANY_ID,
                        #"CompanyName": company.NAME,
                        #"Copacker": company.COPACKER,
                        #"Status": company.STATUS,
                        #"Active": company.ACTIVE,
                        # Add other relevant fields as needed
                    }
                else:
                    company_details = {"Error": f"Company with ID {company_id} not found in COMPANY_TB"}
                row.ResultData = json.dumps(company_details)
        else:
            pass
            # Company does not exist - Create a new record and store the ID in results

    def generate_owns(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
        # Generate OWNS record after ResolveCompany and ResolvePlant tasks are completed
        company_id = None
        plant_id = None
        task_instance = logic_row.row
        application_id = task_instance.ApplicationId
        application = models.WFApplication.query.filter_by(ApplicationID=application_id).first()    
        if not application:
            logic_row.log(f"unable to generate owns - application not found for ApplicationId: {application_id}")
            return False
        task_instances = models.TaskInstance.query.filter_by(ApplicationId=application.ApplicationID).all()
        for task_instance in task_instances:
            task_def = task_instance.TaskDefinition
            if task_def.TaskName == 'ResolveCompany':
                company_id = task_instance.Result
            if task_def.TaskName == 'ResolvePlant':
                plant_id = task_instance.Result
        if company_id is None or plant_id is None:
            logic_row.log(f"unable to generate owns - missing company_id: {company_id} or plant_id: {plant_id}")
            return False
        owns = oukash_models.OWNSTB.query.filter_by(COMPANY_ID=company_id, PLANT_ID=plant_id).first()
        if not owns:
            logic_row.log(f"OWNS record does not exist for company_id: {company_id} and plant_id: {plant_id}")
            return True
        row.ResultData = f"Create OWNS {owns.ID} record"
        #row.Result = owns.ID if owns else None
        return True
    
    def create_application(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow) -> bool:
        #Create an EventAction for the given TaskInstanceId and EventKey
        if logic_row.ins_upd_dlt == 'upd' and old_row and row.Status == old_row.Status and row.Status == 'COMPLETED':
            return True  # Only create application on new OWNS record
        result_data = parse_sqlserver_json(row.ResultData) if row.ResultData and isinstance(row.ResultData, str) else {}
        company_id = None
        plant_id = None
        owns_id = None
        task_instance = logic_row.row
        task_def = task_instance.TaskDefinition
        if 'ResolvePlant' in task_def.TaskName :
            plant_id = row.Result if row.Result is not None else None
            application_id = task_instance.ApplicationId
            application = models.WFApplication.query.filter_by(ApplicationID=application_id).first()    
            # Only create new application when submission task is completed
            if application and application.ApplicationType != 'SUBMISSION' and task_instance.Status != 'COMPLETED':
                return True
            task_instances = models.TaskInstance.query.filter_by(ApplicationId=application.ApplicationID).all()
            owns_task_instance = None
            for task_instance in task_instances:
                task_def = task_instance.TaskDefinition
                if task_def.TaskName == 'ResolveCompany':
                    company_id = task_instance.Result
       
            if not owns_id:
                owns = oukash_models.OWNSTB.query.filter_by(COMPANY_ID=company_id, PLANT_ID=plant_id).first()
                if not owns: 
                    logic_row.log(f"unable to create application - no OWNS record for company_id: {company_id} and plant_id: {plant_id}")
                    return False
                owns_id = owns.ID
            if owns_id and owns_id  != 0:
                app_logger.info(f"Created OWNS record with ID {owns_id} for company_id {company_id} and plant_id {plant_id}")   
                # Call the API endpoint to create the application
                #create_application_from_owns(owns_id=owns.ID, logic_row=logic_row)
                application = models.WFApplication.query.filter_by(ApplicationID=row.ApplicationId).first()
                if application:
                    new_application = models.WFApplication(
                        ApplicationNumber=owns_id,
                        CompanyID=company_id,
                        PlantID=plant_id,
                        ApplicationType='WORKFLOW',
                        Status='NEW',
                        ExternalAppRef=application.ExternalAppRef,
                        WFLinkedApp=application.ApplicationID,
                    )
                    wfapp = create_wfapplication(new_application, owns_id=owns_id, logic_row=logic_row)
                    print(wfapp)
                    result_data["WFID"] = wfapp.get("ApplicationID") if wfapp else None
                    result_data['OWNSID'] = owns_id
                row.ResultData = json.dumps(result_data)
    
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
    def restart_nda_task(task_instance: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
        prior_task = find_next_task_by_name(task_instance, "Upload NDA from Company")
        if prior_task and prior_task.Status == "COMPLETED":
            prior_task.Status = "PENDING"
            prior_task.Result = None
            prior_task.ResultData = None
            prior_task.CompletedDate = None
            logic_row.update(reason="RestartUpload NDA from Company task due to Legal Review changes", row=prior_task)
            app_logger.info(f"Restarted 'Upload NDA from Company' task (TaskInstanceId: {prior_task.TaskInstanceId}) due to changes in Legal Review task (TaskInstanceId: {task_instance.TaskInstanceId})")
            task_instance.Status = "NEW"
    def update_stages(row: models.TaskInstance, old_row: models.TaskInstance , logic_row:LogicRow):
        """
        Update the status of the workflow application
        """
        # Only process updates where status actually changed
        if logic_row.ins_upd_dlt != 'upd':
            return
        if old_row and row.Status == old_row.Status:
            return  # Status didn't change, nothing to do
        row.ActiveStartDate = datetime.datetime.now() if row.Status == 'PENDING' and old_row.Status == 'NEW' else None
        application_id = row.ApplicationId
        application = models.WFApplication.query.filter_by(ApplicationID=application_id).one_or_none()
        task_def = row.TaskDefinition
        if task_def.TaskName == 'AssignNCRC' and row.Status == 'COMPLETED':
            if application is not None:
                application.Status = 'INP'
                application.StartedDate = datetime.datetime.now()
                logic_row.update(reason="Update application status to INP", row=application)
        elif 'ResolvePlant' in task_def.TaskName and row.Status == 'COMPLETED' and old_row.Status != 'COMPLETED' and row.IsVisible == 1:
            resolve_plant(row, old_row, logic_row=logic_row)
        elif 'ResolveCompany' in task_def.TaskName and row.Status == 'COMPLETED' and old_row.Status != 'COMPLETED':
            resolve_company(row, old_row, logic_row=logic_row)
            application.Status =  'INP' if application.Status == 'NEW' else application.Status
            application.CompletedDate = datetime.datetime.now()
            logic_row.update(reason=f"Update application status to {application.Status}", row=application)
        elif 'CreateOwns' in task_def.TaskName and row.Status == 'COMPLETED' and old_row.Status != 'COMPLETED':
            generate_owns(row, old_row, logic_row=logic_row)
        elif "Legal Review" in task_def.TaskName and row.Status == "IN_PROGRESS":
            restart_nda_task(task_instance=row, old_row=old_row, logic_row=logic_row)
        elif task_def.TaskName == 'End Certification' and row.Status == 'COMPLETED':
            if application is not None:
                application.Status = 'WTH' if application.Status == 'WTH' else 'COMPL'
                application.CompletedDate = datetime.datetime.now()
                logic_row.update(reason=f"Update application status to {application.Status}", row=application)
        elif task_def.TaskName.upper() == 'INTAKE APP END' and row.Status == 'COMPLETED':
            if application is not None:
                application.CompletedDate = datetime.datetime.now()
                application.Status = 'COMPL'
                logic_row.update(reason=f"Update application status to {application.Status}", row=application)
        elif task_def.TaskName == 'GenerateWFApplication' and row.Status == 'COMPLETED':
            #create_application(row, old_row, logic_row=logic_row)
            #lookup new wf application linked to this ExternalAppRef/Plant
            pass
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
            elif TaskName == 'Cancel Application' and row.Result == 'YES': status = 'WTH'
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

    def generate_primary_key(row: oukash_models.PLANTTB, old_row: oukash_models.PLANTTB, logic_row: LogicRow):
        # This is an example of an early row event to generate a primary key value for PLANTTB
        # In practice, you would typically use an IDENTITY column or a database sequence for this purpose
        if logic_row.ins_upd_dlt == 'ins' and (row.PLANT_ID is None or row.PLANT_ID == 0):
            max_id = logic_row.session.query(oukash_models.PLANTTB).order_by(oukash_models.PLANTTB.PLANT_ID.desc()).first()
            row.PLANT_ID = (max_id.PLANT_ID + 1) if max_id and max_id.PLANT_ID else 1
            logic_row.log(f"Generated PLANT_ID {row.PLANT_ID} for new PLANTTB record")
    Rule.early_row_event(oukash_models.PLANTTB, calling=generate_primary_key)

    Rule.after_flush_row_event(on_class=models.TaskInstance, calling=create_application)