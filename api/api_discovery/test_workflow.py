
from flask_jwt_extended import get_jwt, jwt_required
from api.api_discovery.assign_role import _assign_role   
import datetime
from database.models import WFApplication, TaskInstance
from database.oukash_models import CompanyApplication
import database.models as models
from flask import request, jsonify
import logging
import safrs
from security.system.authorization import Security
from sqlalchemy.sql import text
from types import SimpleNamespace
import time
from database.cache_service import DatabaseCacheService


"""
Various endpoints to test workflow functionality and cleanup or reset tests
"""
db = safrs.DB 
session = db.session
access_token = None
completed_by = None
app_logger = logging.getLogger("api_logic_server_app")

cache = DatabaseCacheService.get_instance()

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass

    @app.route('/whoami', methods=['GET'])
    @jwt_required()
    def whoami():
        info = Security.extract_roles_and_delegated()
        return jsonify({
            "roles": info['roles'],
            "delegated": info['app:delegated'],
            "username": info['username']
        })

    @app.route('/run_workflow_to_completion', methods=['GET','POST','OPTIONS'])
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
    @jwt_required()
    def reset_task_instances(application_id):
        # Implement reset logic here
        access_token = request.headers.get("Authorization")
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application ID: {application_id} not found'}), 404
        do_reset(application_id)
        #from api.api_discovery.complete_task_optimized import _complete_task_optimized as _complete_task
        from api.api_discovery.complete_task import _complete_task
        start_instance_id = get_start_task(application_id)
        if not start_instance_id:
            return jsonify({"result": f'Start TaskInstance not found for Application ID: {application_id}'}), 404   
        _complete_task(start_instance_id, 'Started', 'system', 'Workflow started', access_token)
    
        role_assignment = models.RoleAssigment(
            ApplicationId=application.ApplicationID,
            Role="DISPATCH",
            Assignee="system",
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

def find_all_stages_for_application(application_id):
    all_tasks = TaskInstance.query.filter(TaskInstance.ApplicationId == application_id).order_by(TaskInstance.TaskInstanceId).all()
    stages = []
    for task in all_tasks:
        stage = task.Stage
        if stage and stage not in stages:
            stages.append(stage)
    return stages

def find_all_pending_tasks(application_id: int, stage_id: int):
    """
    Find all pending tasks for a given stage, excluding SYSTEM (internal) tasks.
    
    """
    pending_tasks = []
    response = session.query(models.TaskInstance).filter(models.TaskInstance.ApplicationId == application_id, models.TaskInstance.StageId == stage_id, models.TaskInstance.Status == 'PENDING').order_by(models.TaskInstance.TaskInstanceId).all()
    pending_tasks.extend([task for task in response])
    for task_instance in pending_tasks:
        taskDef = task_instance.TaskDefinition
        task_name = taskDef.TaskName if taskDef else 'Unknown'
        if task_instance and taskDef and taskDef.AssigneeRole.upper() == 'SYSTEM':
            print(f'Skipping System Task {task_name} - {task_instance} Role: {taskDef.AssigneeRole}')
            pending_tasks.remove(task_instance)
    return pending_tasks

def find_stage_end(application_id: int, stage_id: int):
    task_instances = session.query(models.TaskInstance).filter(models.TaskInstance.ApplicationId == application_id, models.TaskInstance.StageId == stage_id).all()
    for task_instance in task_instances:
        if task_instance.TaskDefinition.TaskType == 'STAGEEND':
            return task_instance.Status
    return "NEW"

def find_task_flow(task_instance:TaskInstance):
    #task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
    if not task_instance:
        app_logger.error(f'TaskInstance not found: {task_instance.TaskInstanceId}')
        return []

    # Go To TaskFlow from TaskId and check to see if all the prior states are completed
    task_def = task_instance.TaskDefinition
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
    #from api.api_discovery.complete_task_optimized import _complete_task_optimized as _complete_task
    from api.api_discovery.complete_task import _complete_task
    task_instance_id = task_instance.TaskInstanceId
    task_name = task_instance.TaskDefinition.TaskName
    if task_instance.TaskDefinition.TaskType == 'END':
        app_logger.info(f'Skipping completion of END Task: {task_name} - {task_instance_id}')
        return
    #access_token = request.headers.get("Authorization") if access_token is None else access_token
    result = result_scenario(task_name, scenario)
    response = _complete_task(task_instance_id=task_instance_id, result=result, completed_by=completed_by, completion_notes='Task completed successfully', access_token=access_token, depth=0)
    app_logger.info(f'Complete Task {task_name}: {task_instance_id} response: {response}')
    print(f"Complete Task {task_name} - Result - {result}  -Response: {response}")
    time.sleep(1)

def result_scenario(task_name, scenario: int = 1) -> str:
    if scenario == 2:
        result = 'YES' if "to Withdrawn Y/N" in task_name else None
    else:
        result = 'NO' if "to Withdrawn Y/N" in task_name else None
    result = 'NO' if "Withdraw Application" in task_name else result
    result = 'YES' if "Company requires NDA" in task_name else result
    result = 'YES' if "Is Inspection Needed" in task_name else result
    result = '2025-11-01' if "Schedule" in task_name else result
    result = 1000 if "Assign Invoice Amount" in task_name else result
    return result

def run_workflow_to_completion(application: WFApplication, user: str, scenario: int = 1, access_token: str = None):
    if not application:
        app_logger.error(f'Application not found for Application ID: {application_id}')
        return
    application_id = application.ApplicationID
    stages_list = find_all_stages_for_application(application_id)
    completed_tasks = []
    results = []
    task_definitions = cache.get_all_task_definitions()
    for stage in stages_list:
        stage_id = stage.StageId
        status = get_stage_status(find_all_tasks_for_stage(application_id, stage_id), task_definitions) # "'IN_PROGRESS'"
        name = getattr(stage,'StageName')
        app_logger.info(f'Start Processing Stage: {name} - {stage_id} Status: {status}')
        if name == 'Initial':
            pending_tasks = find_all_pending_tasks(application_id, stage_id)
            #while len(pending_tasks) > 0 and find_lane_end(stage_id) != 'COMPLETED':
            for task_instance in pending_tasks:
                if task_instance.TaskDefinition.TaskName == 'AssignNCRC' and task_instance.Status == 'PENDING':
                    _assign_role(task_id=task_instance.TaskInstanceId, role='NCRC',assignee=completed_by, app_id=application_id,  user=completed_by, access_token=access_token)
                    print(f'  Assign Role: {task_instance.TaskDefinition.TaskName}')
        if name == 'Initial':
            pending_tasks = find_all_pending_tasks(application_id, stage_id)
            for task_instance in pending_tasks:
                print(f'  Completing Task: {task_instance.TaskDefinition.TaskName}')
                complete_task(task_instance)
                completed_tasks.append({"TaskInstanceId": task_instance.TaskInstanceId,"TaskName": task_instance.TaskDefinition.TaskName})
                pending_tasks.remove(task_instance)
                pending_tasks.extend(find_all_pending_tasks(application_id, stage_id))

        elif name == 'NDA':
             process_all_pending_tasks(application_id, stage_id=stage_id, completed_tasks=completed_tasks)

        elif name == 'Inspection':
            pending_tasks = find_all_pending_tasks(application_id, stage_id)
            while len(pending_tasks) > 0 and find_stage_end(application_id, stage_id=stage_id) != 'COMPLETED':
                for task_instance in pending_tasks:
                    if task_instance.TaskDefinition.TaskName == 'Mark Invoice Paid':
                        from api.api_discovery.event_action import _resolve_event
                        event_action = session.query(models.EventAction.EventKey).filter(models.EventAction.TaskInstanceId == task_instance.TaskInstanceId).first()
                        if event_action:
                            event_key = getattr(event_action, 'EventKey')
                            _resolve_event(event_key, user=user, logic_row=None, access_token=access_token)
                            print(f'  Resolving EventAction for Task: {task_instance.TaskDefinition.TaskName} EventKey: {event_key}')
                    else:
                        # For testing, we auto-complete the scheduling task
                        complete_task(task_instance)
                        completed_tasks.append({"TaskInstanceId": task_instance.TaskInstanceId,"TaskName": task_instance.TaskDefinition.TaskName})
                pending_tasks = find_all_pending_tasks(application_id, stage_id)

        elif name == 'Ingredients':
             process_all_pending_tasks(application_id,stage_id=stage_id, completed_tasks=completed_tasks)
                
        elif name == 'Products':
             process_all_pending_tasks(application_id, stage_id=stage_id, completed_tasks=completed_tasks)

        elif name == 'Contract':
             process_all_pending_tasks(application_id, stage_id=stage_id, completed_tasks=completed_tasks)

        elif name == 'Certification':
            process_all_pending_tasks(application_id, stage_id=stage_id, completed_tasks=completed_tasks)

        print_application_status(application_id, name)
        status = get_stage_status(find_all_tasks_for_stage(application_id, stage_id), task_definitions) # "'IN_PROGRESS'"
        name = getattr(stage,'StageName')
        results.append({"Stage": name, "Status": status})
    
        
    print(f"Workflow for application {application_id} completed {completed_tasks}.")
    return results, completed_tasks

def print_application_status(application_id: int,stageName: str):
    application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
    if application:
        app_logger.info(f'Application {application_id} StageName: {stageName} Status: {application.Status}')
        print(f'Application {application_id} StageName: {stageName} Status: {application.Status}')

def find_all_tasks_for_stage(application_id, stage_id) -> list:
    all_tasks = TaskInstance.query.filter(TaskInstance.ApplicationId == application_id, TaskInstance.StageId == stage_id).order_by(TaskInstance.TaskInstanceId).all()
    return [task.to_dict() for task in all_tasks]

def process_all_pending_tasks(application_id: int, stage_id:int, completed_tasks: list):
    pending_tasks = find_all_pending_tasks(application_id, stage_id)
    while len(pending_tasks) > 0 and find_stage_end(application_id, stage_id) != 'COMPLETED':
        for task_instance in pending_tasks:
            print(f'  Completing Task: {task_instance.TaskDefinition.TaskName}')
            complete_task(task_instance)
            completed_tasks.append({"TaskInstanceId": task_instance.TaskInstanceId,"TaskName": task_instance.TaskDefinition.TaskName})
            pending_tasks.remove(task_instance) 
            pending_tasks.extend(find_all_pending_tasks(application_id, stage_id))
            app_id = task_instance.ApplicationId
            status = WFApplication.query.filter_by(ApplicationID=app_id).first().Status
            if status == 'COMPL':
                app_logger.info(f'Application {app_id} completed for Stage {stage_id}.')
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

    contact = SimpleNamespace(**contacts[0]) if contacts else None
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


def get_stage_status(tasks: list, task_definitions: dict) -> str:
    """
    Determines the overall status of a stage based on its tasks.
    """
    status = 'NEW'
    if not tasks or len(tasks) == 0:
        return status
    stage_start = False
    stage_end = False
    for task in tasks:
        taskdef_id = task['TaskDefinitionId']
        taskdef = task_definitions.get(taskdef_id).to_dict() if taskdef_id in task_definitions else {}
        if len(taskdef) == 0:
            continue
        
        if task['Status'] in ['COMPLETED']: # could we add PENDING as well?? TODO count_pending            
            if taskdef and taskdef['TaskType'] in ['START',"STAGESTART"]:
                stage_start = True
            elif taskdef and taskdef['TaskType'] in ['END','STAGEEND']:
                stage_end = True
            

    if stage_start and not stage_end:
        return "IN_PROGRESS"
    if stage_start and stage_end:
        status = "COMPLETED"
    else:
        status = "NEW"
    return status