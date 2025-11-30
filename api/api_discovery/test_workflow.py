from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from api.api_discovery.assign_role import _assign_role   
import datetime
from database.models import StageInstance, WFApplication, TaskInstance
import database.models as models
from flask import request, jsonify
import logging
import safrs
from security.system.authorization import Security
from sqlalchemy.sql import text
from types import SimpleNamespace
import time

"""
Various endpoints to test workflow functionality and cleanup or reset tests
"""
db = safrs.DB 
session = db.session
access_token = None
completed_by = None
app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass

    def admin_required():
        """
        Support option to bypass security (see cats, below).
        """
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                if Args.instance.security_enabled == False:
                    return fn(*args, **kwargs)
                verify_jwt_in_request(True)  # must be issued if security enabled
                return fn(*args, **kwargs)
            return decorator
        return wrapper

    @app.route('/run_workflow_to_completion', methods=['GET','POST','OPTIONS'])
    @admin_required()
    @jwt_required()
    def run_workflow_to_completion_endpoint():
        '''
        Invoke-RestMethod -Uri "http://localhost:5656/run_workflow_to_completion?application_id=1" -Method GET -ContentType "application/json" -Headers @{Authorization = "Bearer {<your_jwt_token>}
        '''
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        global access_token
        access_token = request.headers.get("Authorization")
        args = request.args
        global completed_by
        user = Security.current_user().Username
        completed_by =user
        application_id = args.get('application_id') or args.get('applicationId') or args.get('applicationID') or None
        scenario = args.get('scenario', 1)      
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application with ApplicationID: {application_id} not found'}), 404
        results, completed_tasks = run_workflow_to_completion(application, user=completed_by, scenario=scenario, access_token=access_token)
        return jsonify({"result": f"Workflow for application {application_id} completed {completed_tasks}. Stages: {results}"})
    
    @app.route('/reset_task_instances/<application_id>', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def reset_task_instances(application_id):
        # Implement reset logic here
        global access_token
        access_token = request.headers.get("Authorization")
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application ID: {application_id} not found'}), 404
        do_reset(application_id)
        from api.api_discovery.complete_task import _complete_task
        start_instance_id = get_start_task(application_id)
        if not start_instance_id:
            return jsonify({"result": f'Start TaskInstance not found for Application ID: {application_id}'}), 404   
        _complete_task(start_instance_id, 'Started', 'system', 'Workflow started', access_token)
    
        role_assignment = models.RoleAssignment(
            ApplicationId=application.ApplicationID,
            Role="DISPATCH",
            Assignee="SYSTEM",
            CreatedDate=datetime.datetime.now(datetime.timezone.utc).date()
        )
        session.add(role_assignment)
        session.commit()
        return jsonify({"result": f'Reset initiated for Application ID: {application_id}'})
def start_workflow(application_id: int, start_by: str):
    from api.api_discovery.start_workflow import _start_workflow_async
    process_name = "OU Application Init"
    response = _start_workflow_async(process_name, int(application_id), start_by, "NORMAL")
    return response['process_instance_id']


def find_all_stages_for_process(application_id: int):
    stages = StageInstance.query.filter(StageInstance.ApplicationId == application_id).order_by(StageInstance.StageId).all()
    return [stage for stage in stages]

def find_all_pending_tasks(stage_id: int):
    """
    Find all pending tasks for a given stage, excluding SYSTEM (internal) tasks.
    
    """
    pending_tasks = []
    response = session.query(models.TaskInstance).filter(models.TaskInstance.StageId == stage_id, models.TaskInstance.Status == 'PENDING').order_by(models.TaskInstance.TaskInstanceId).all()
    pending_tasks.extend([task for task in response])
    for task_instance in pending_tasks:
        taskDef = task_instance.TaskDef
        task_name = taskDef.TaskName if taskDef else 'Unknown'
        if task_instance and taskDef and (taskDef.AssigneeRole.upper() == 'SYSTEM' or taskDef.AutoComplete == True):
            print(f'Skipping System Task {task_name} - {task_instance} Role: {taskDef.AssigneeRole} AutoComplete: {taskDef.AutoComplete}')
            pending_tasks.remove(task_instance)
    return pending_tasks

def get_stage_end_status(stage_id: int):
    stage = session.query(models.StageInstance).filter(models.StageInstance.StageInstanceId == stage_id).first()
    if not stage:
        app_logger.error(f'StageInstance not found: {stage_id}')
        return 'NONE'
    task_instances = session.query(models.TaskInstance).filter(models.TaskInstance.StageId == stage_id).all()
    for task_instance in task_instances:
        if task_instance.TaskDef.TaskType == 'STAGEEND':
            return task_instance.Status
    return "NEW"

def find_task_flow(task_instance:TaskInstance):
    #task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
    if not task_instance:
        app_logger.error(f'TaskInstance not found: {task_instance.TaskInstanceId}')
        return []

    # Go To TaskFlow from TaskId and check to see if all the prior states are completed
    task_def = task_instance.TaskDef
    if not task_def:
        app_logger.error(f'TaskDefinition not found: {task_instance.TaskId}')
        return []

    task_name = task_def.TaskName
    #stages_list = find_all_stages_for_process(task_instance.Stage.ProcessInstance.ProcessId)
    app_logger.info(f'Completing TaskInstance: {task_instance.TaskInstanceId} - {task_name}')
    task_flows_from = task_def.ToTaskTaskFlowList or []
    task_flows_to = task_def.TaskFlowList or []
    return task_flows_to

def complete_task(task_instance, scenario: int = 1):
    from api.api_discovery.complete_task import _complete_task
    task_instance_id = task_instance.TaskInstanceId
    task_name = task_instance.TaskDef.TaskName
    #access_token = request.headers.get("Authorization") if access_token is None else access_token
    result = result_scenario(task_name, scenario)
    response = _complete_task(task_instance_id=task_instance_id, result=result, completed_by=completed_by, completion_notes='Task completed successfully', access_token=access_token, depth=0)
    app_logger.info(f'Complete Task {task_name}: {task_instance_id} response: {response}')
    if result:
        time.sleep(1)
    print(f"Complete Task {task_name} - Response: {response}")

def result_scenario(task_name, scenario: int = 1) -> str:
    if scenario == 2:
        result = 'YES' if "to Withdrawn Y/N" in task_name else None
    else:
        result = 'NO' if "to Withdrawn Y/N" in task_name else None
    result = 'NO' if "Withdraw Application" in task_name else result
    result = 'YES' if "Needs NDA" in task_name else result
    result = 'YES' if "Is Inspection Needed" in task_name else result
    result = '2025-11-01' if "Schedule" in task_name else result
    result = 1000 if "Assign Invoice Amount" in task_name else result
    return result

def run_workflow_to_completion(application: WFApplication, user: str, scenario: int = 1, access_token: str = None):
    application_id = application.ApplicationID
    stages_list = find_all_stages_for_process(application.ApplicationID)
    completed_tasks = []
    for stage in stages_list:
        stage_id = stage.StageInstanceId
        stage_state = session.query(models.StageInstance).filter(models.StageInstance.StageInstanceId == stage_id).first()
        status = stage_state.Status # "'IN_PROGRESS'"
        name = stage.Stage.StageName if stage else 'Unknown'
        app_logger.info(f'Start Processing Stage: {name} - {stage_id} Status: {status}')
        if status in ['NEW','IN_PROGRESS'] and name == 'Initial':
            pending_tasks = find_all_pending_tasks(stage_id)
            for task_instance in pending_tasks:
                if task_instance.TaskDef.TaskName == 'AssignNCRC':
                    _assign_role(task_instance.TaskInstanceId, role='NCRC', assignee=completed_by, application_id=application_id, user=completed_by, access_token=access_token)
                    print(f'  Assign Role: {task_instance.TaskDef.TaskName}')
            process_stage(stage_id, completed_tasks)

        elif status in ['NEW','IN_PROGRESS'] and name == 'NDA':
            process_stage(stage_id, completed_tasks)
            
        elif status in ['NEW','IN_PROGRESS'] and name == 'Inspection':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0 and get_stage_end_status(stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    if task_instance.TaskDef.TaskName == 'Mark Invoice Paid':
                        from api.api_discovery.event_action import _resolve_event
                        event_key = "INVOICE_98286" 
                        _resolve_event(event_key, user, access_token)
                        print(f'  Resolving EventAction for Task: {task_instance.TaskDef.TaskName} EventKey: {event_key}')
                process_stage(stage_id, completed_tasks)

        elif status in ['NEW','IN_PROGRESS'] and name == 'Ingredients':
            process_stage(stage_id, completed_tasks)

        elif status in ['NEW','IN_PROGRESS'] and name == 'Products':
            process_stage(stage_id, completed_tasks)
                    
        elif status in ['NEW','IN_PROGRESS'] and name == 'Contract':
            process_stage(stage_id, completed_tasks)

        elif status in ['NEW','IN_PROGRESS'] and name == 'Certification':
            process_stage(stage_id, completed_tasks)

    stage_list = find_all_stages_for_process(application_id=application.ApplicationID)
    results = []
    for stage in stage_list:
        results.append({"Stage": stage.Stage.StageName, "Status": stage.Status})
    print(f"Workflow for application {application_id} completed {completed_tasks}.")
    return results, completed_tasks

def process_all_pending_tasks(stage_id: int, completed_tasks: list):
    pending_tasks = find_all_pending_tasks(stage_id)
    while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
        for task_instance in pending_tasks:
            print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
            complete_task(task_instance)
            completed_tasks.append(task_instance.TaskInstanceId)
            pending_tasks = find_all_pending_tasks(stage_id)
            app_id = task_instance.Stage.ProcessInstance.ApplicationId
            status = WFApplication.query.filter_by(ApplicationID=app_id).first().Status
            if status == 'COMPL':
                app_logger.info(f'Application {app_id} already completed. Skipping stage {stage_id}.')
                return

def process_task_flow(task_instance, stage_instance_id, completed_tasks):
    task_flow_instances = find_task_flow(task_instance)
    for task_flow in task_flow_instances:
        next_task_def = session.query(models.TaskDefinition).filter(models.TaskDefinition.TaskId == task_flow.ToTaskId).first()
        if next_task_def and next_task_def.AssigneeRole != 'SYSTEM' and task_instance.Status == 'COMPLETED':
            next_task_instance = session.query(models.TaskInstance).filter(models.TaskInstance.TaskId == next_task_def.TaskId, models.TaskInstance.StageId == stage_instance_id).first()
            if next_task_instance and next_task_instance.Status in ['NEW','PENDING'] and next_task_instance.TaskInstanceId not in completed_tasks:
                print(f'      Next Task to complete: {next_task_def.TaskName} Status: {next_task_instance.Status}')
                complete_task(next_task_instance)
                completed_tasks.append(next_task_instance.TaskInstanceId)
                process_task_flow(next_task_instance, stage_instance_id, completed_tasks)

def process_stage(stage_id, completed_tasks):
    pending_tasks = find_all_pending_tasks(stage_id)
    while len(pending_tasks) > 0 and get_stage_end_status(stage_id) != 'COMPLETED':
        for task_instance in pending_tasks:
            print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
            complete_task(task_instance)
            completed_tasks.append(task_instance.TaskInstanceId)
            pending_tasks = find_all_pending_tasks(stage_id)
        
def do_reset(application_id):
    session.execute(text(f"""
        UPDATE TaskInstances SET Status = 'NEW', Result = NULL, ResultData = NULL, ErrorMessage = NULL 
        WHERE StageId IN (SELECT StageInstanceId FROM StageInstance WHERE ProcessInstanceId = 
            (SELECT InstanceId FROM ProcessInstances WHERE ApplicationId = {application_id})
        );
       
        UPDATE StageInstance SET Status = 'NEW' 
        WHERE ProcessInstanceId IN 
            (SELECT InstanceId FROM ProcessInstances WHERE ApplicationId = {application_id});
        

        UPDATE ProcessInstances SET Status = 'NEW' 
        WHERE ApplicationId = {application_id};
        

        UPDATE WFApplication SET Status = 'NEW' 
        WHERE ApplicationId = {application_id};
       
    """))
    session.commit()

def get_start_task(application_id):
    #start_task = session.query(models.TaskDefinition).filter(models.TaskDefinition.ProcessId == process_id, models.TaskDefinition.AssigneeRole == 'SYSTEM').first()
    response = session.execute(text(f"""
        select TaskInstanceId
            FROM [dashboard].[dbo].[TaskInstances] ti,
            [dashboard].[dbo].[TaskDefinitions] td
            where ti.TaskId = td.TaskId
            and td.TaskType = 'START'
            and  ti.StageId in (
                Select StageInstanceId from StageInstance where ProcessInstanceId = 
                (Select InstanceId from ProcessInstances where ApplicationId = {application_id})
            )
    """))
    row = response.fetchone()
    return row[0] if row else None

def create_new_application_from_owns(owns_instance):
    plant = owns_instance.PLANT_TB
    company = owns_instance.COMPANY_TB
    contacts = get_contact(company.COMPANY_ID, plant.PLANT_ID)
    has_product_count = has_products(company.COMPANY_ID, plant.PLANT_ID)
    if not has_product_count:
        app_logger.error(f'No products found for company {company.COMPANY_ID} plant {plant.PLANT_ID}. Cannot create application.')
        return None

    contact = None #SimpleNamespace(**contacts[0]) if contacts else None
    '''
    applicationNumber =  1 + CompanyApplication.query.count()
    application = CompanyApplication(
        PreviousCertification='N',
        OUCertified='Y',
        CurrentlyCertified='Y',
        CompanyID=getattr(company, 'COMPANY_ID', 0),
        CompanyName=getattr(company, 'COMPANY_NAME', getattr(company, 'NAME', '')),
        PlantName=getattr(plant, 'NAME', ''),
        Street1=getattr(company, 'STREET1', getattr(plant, 'STREET1', '')),
        Street2=getattr(company, 'STREET2', getattr(plant, 'STREET2', '')),
        City=getattr(company, 'CITY', getattr(plant, 'CITY', '')),
        State=getattr(company, 'STATE', getattr(plant, 'STATE', '')),
        Zip=getattr(company, 'ZIP', getattr(plant, 'ZIP', '')),
        Country=getattr(company, 'COUNTRY', getattr(plant, 'COUNTRY', '')),
        title=getattr(contact,'Title') if contact else '',
        FirstName=getattr(contact,'FirstName') if contact else '',
        LastName=getattr(contact,'LastName') if contact else '',
        email=getattr(contact,'EMail') if contact else '',
        phone=getattr(contact,'Voice') if contact else '',
        NatureOfProducts='',
        HowHeardAboutUs='GENERATED',
        Comments='',
        Description='Created from OWNS record',
        OtherCertification='',
        gclid='',
        utm_source='',
        utm_medium='',
        utm_campaign='',
        dateSubmitted=datetime.datetime.now(datetime.timezone.utc).date(),
        Utm_Term='',
        Version='NEWAPI',
        Language='ENGLISH',
        Oukosher_source='',
        JotFormSubmissionID=''
    )
    session.add(application)
    session.commit()
    '''
    application = session
    return application

def has_products(company_id:int, plant_id: int) -> bool:
    sql = f"""
        SELECT TOP (1) [PRODUCT_NAME]
        FROM [ou_kash].[dbo].[PRODUCT_GRID]
            where [COMPANY_ID] = {company_id}
            and [PLANT_ID] = {plant_id}
    """
    result = session.execute(text(sql))
    products = result.fetchall()
    return len(products) > 0

def get_contact(company_id:int, plant_id: int):
    sql = f"""
        SELECT TOP (1) [pcID]
            ,[companytitle]
            ,[owns_ID]
            ,[Title]
            ,[FirstName]
            ,[LastName]
            ,[Voice]
            ,[Fax]
            ,[EMail]
            ,[Cell]
            ,[PrimaryCT]
            ,[BillingCT]
            ,[WebCT]
            FROM [ou_kash].[dbo].[PlantContacts]
                WHERE owns_ID IN
                (select TOP 1 OWNS_ID from [ou_kash].[dbo].[OWNS_TB] where COMPANY_ID = {company_id} and PLANT_ID = {plant_id})
    """
    result = session.execute(text(sql))
    contacts = result.fetchall()
    if not contacts:
        app_logger.error(f'Contact not found: {company_id} {plant_id}')
        return None
    rows = [dict(zip(row._fields, row)) for row in contacts]
    return rows