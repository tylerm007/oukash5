from functools import wraps
from api.api_discovery import assign_role
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from api.api_discovery.assign_role import _assign_role   

from urllib import response
from database.models import StageInstance, WFApplication, TaskInstance, TaskDefinition, ProcessInstance
import database.models as models
from flask import request, jsonify
import requests
import logging
import safrs
from sqlalchemy.sql import text
"""
Various endpoints to test workflow functionality and cleanup or reset tests
"""
db = safrs.DB 
session = db.session

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

    @app.route('/hello_newer_service')
    def hello_newer_service():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://localhost:5656/hello_newer_service?user=ApiLogicServer
        """
        user = request.args.get('user')
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello from even_newer_service! from {user}'})
    
    @app.route('/test_parser', methods=['GET'])
    #jwt_required()
    def test_parser():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://localhost:5656/test_parser?filter={"and":[{"name":{"like":"%a%"}}]}
                Invoke-RestMethod -Uri "http://localhost:5656/test_parser" -Method GET -ContentType "application/json"
        """
        filter = request.args.get('filter')
        app_logger.info(f'filter: {filter}')
        import requests
        filter1 =  '[{"name":"ACTIVE","op":"eq","val":1},{"name":"RC","op":"ilike","val":"%Gorelik%"},{"name":"CATEGORY","op":"ilike","val":"%Nut%"},{"name":"NAME","op":"ilike","val":"%Company%"}]'
        endpoint = "COMPANYTB"
        response = requests.get(f'http://localhost:5656/api/{endpoint}?filter={filter1}')

        endpoint = "PLANTTB"
        filter2 =  '[{"name":"ACTIVE","op":"eq","val":1},{"name":"LABEL_SEQ_NUM","op":"gt","val":1}]'
        response2 = requests.get(f'http://localhost:5656/api/{endpoint}?filter={filter2}')

        endpoint = "COMPANYTB" 
        filter3 = '[{"name":"ACTIVE","op":"eq","val":1},{"name":"RC","op":"ilike","val":"%Gorelik%"},{"name":"STATUS","op":"eq","val":"Certified"}]'
        response3 = requests.get(f'http://localhost:5656/api/{endpoint}?filter={filter3}')
        return jsonify({"result": f'filter: {filter}', "response": response.json(), "response2": response2.json(), "response3": response3.json()})

    @app.route('/create_application', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def create_application_endpoint():

        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        args = request.args
        user = get_jwt().get("sub", "admin")
        applicationNumber = int(args.get('applicationNumber'))
        jot_application = session.query(models.CompanyApplication).filter(models.CompanyApplication.ID == applicationNumber).first()
        if jot_application is None:
            return jsonify({"result": f'Application with ApplicationNumber: {applicationNumber} does not exist with ID: {applicationNumber}'}), 400
        companyID = jot_application.CompanyID
        plantID = None
        plant = session.query(models.PLANTTB).filter(models.PLANTTB.NAME == jot_application.PlantName).first()
        if plant:
            plantID = plant.PLANT_ID
        application_id = create_new_application(applicationNumber, companyID, plantID)
        process_id = start_workflow(application_id, user)
        return jsonify({"result": f'Created application with ID: {application_id}, started process ID: {process_id}'})

    @app.route('/run_workflow_to_completion', methods=['GET','POST','OPTIONS'])
    @admin_required()
    @jwt_required()
    def run_workflow_to_completion_endpoint():
        '''
        Invoke-RestMethod -Uri "http://localhost:5656/run_workflow_to_completion?applicationNumber=1" -Method GET -ContentType "application/json" -Headers @{Authorization = "Bearer {<your_jwt_token>}
        '''
        args = request.args
        user = get_jwt().get("sub", "admin")
        applicationNumber = args.get('applicationNumber')
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationNumber == applicationNumber).first()
        if not application:
            return jsonify({"result": f'Application with ApplicationNumber: {applicationNumber} not found'}), 404
        run_workflow_to_completion(application, user)
        return jsonify({"result": f'Workflow run to completion'})

    @app.route('/reset_task_instances/<application_id>', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def reset_task_instances(application_id):
        # Implement reset logic here
        access_token = request.headers.get("Authorization")
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application ID: {application_id} not found'}), 404
        do_reset(application_id)
        from datetime import datetime
        from api.api_discovery.complete_task import _complete_task
        start_instance_id = get_start_task(application_id)
        if not start_instance_id:
            return jsonify({"result": f'Start TaskInstance not found for Application ID: {application_id}'}), 404   
        _complete_task(start_instance_id, 'Started', 'system', 'Workflow started', access_token)
    
        role_assignment = models.RoleAssigment(
            ApplicationId=application.ApplicationID,
            Role="DISPATCH",
            Assignee="system",
            CreatedDate=datetime.utcnow()
        )
        session.add(role_assignment)
        session.commit()
        return jsonify({"result": f'Reset initiated for Application ID: {application_id}'})

    @app.route('/cleanup_workflow_data/<application_id>', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def cleanup_workflow_data(application_id):
        # Implement cleanup logic here
        application = session.query(models.WFApplication).filter(models.WFApplication.ApplicationID == application_id).first()
        if not application:
            return jsonify({"result": f'Application ID: {application_id} not found'}), 404
        process_instance = session.query(models.ProcessInstance).filter(models.ProcessInstance.ApplicationId == application_id).first()
        process_id = process_instance.InstanceId if process_instance else None
        if not process_instance:
            return jsonify({"result": f'Process ID: {process_id} not found for Application ID: {application_id}'}), 404 
        do_cleanup(application_id, process_id)
        return jsonify({"result": f'Cleanup initiated for Application ID: {application_id}, Process ID: {process_id}'})

def create_new_application(applicationNumber: int, companyID: int, plantID: int):
    from datetime import datetime
    application = WFApplication(
            Name="New Application",
            Description="Description of the new application",
            Status="NEW",
            CompanyID=companyID,
            PlantID=plantID,
            SubmissionDate=datetime.now().isoformat(),
            CreatedBy="tband",
            CreatedDate=datetime.now().isoformat(),
            Priority="HIGH",
            ApplicationNumber=applicationNumber,
            WFDashboardID=1
    )
    session.add(application)
    session.commit()
    app_logger.info(f'Created new application with ID: {application.ApplicationID}')
    return application.ApplicationID


def start_workflow(application_id: int, start_by: str):
    from api.api_discovery.start_workflow import _start_workflow
    process_name = "OU Application Init"
    response = _start_workflow(process_name, int(application_id), start_by, "NORMAL")
    return response['process_instance_id']


def find_all_stages_for_process(process_id):
    stages = StageInstance.query.filter(StageInstance.ProcessInstanceId == process_id).all()
    return [stage for stage in stages]

def find_all_pending_tasks(stage_id: int):
    """
    Find all pending tasks for a given stage, excluding SYSTEM (internal) tasks.
    
    """
    pending_tasks = []
    response = session.query(models.TaskInstance).filter(models.TaskInstance.StageId == stage_id, models.TaskInstance.Status == 'PENDING').all()
    pending_tasks.extend([task for task in response])
    for task_instance in pending_tasks:
        taskDef = task_instance.TaskDef
        task_name = taskDef.TaskName if taskDef else 'Unknown'
        if task_instance and taskDef and taskDef.AssigneeRole.upper() == 'SYSTEM':
            print(f'Skipping System Task {task_name} - {task_instance} Role: {taskDef.AssigneeRole}')
            pending_tasks.remove(task_instance)
    return pending_tasks

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

def complete_task(task_instance):
    from api.api_discovery.complete_task import _complete_task
    task_instance_id = task_instance.TaskInstanceId
    task_name = task_instance.TaskDef.TaskName
    access_token = request.headers.get("Authorization")
    result = 'NO' if "to Withdrawn Y/N" in task_name else None
    result = 'NO' if "Withdraw Application" in task_name else None
    result = 'YES' if "Needs NDA" in task_name else result
    result = 'YES' if "Is Inspection Needed" in task_name else result
    result = '2025-11-01' if "Schedule" in task_name else result
    response = _complete_task(task_instance_id=task_instance_id, result=result, completed_by='tband', completion_notes='Task completed successfully', access_token=access_token, depth=0)
    app_logger.info(f'Complete Task {task_name}: {task_instance_id} response: {response}')

def run_workflow_to_completion(application: WFApplication, user: str):
    application_id = application.ApplicationID
    process_instance = session.query(models.ProcessInstance).filter(models.ProcessInstance.ApplicationId == application_id).first()
    if not process_instance:
        app_logger.error(f'ProcessInstance not found for Application ID: {application_id}')
        return
    process_id = process_instance.InstanceId
    stages_list = find_all_stages_for_process(process_id)
    completed_tasks = []
    for stage in stages_list:
        stage_id = stage.StageInstanceId
        stage_state = session.query(models.StageInstance).filter(models.StageInstance.StageInstanceId == stage_id).first()
        status = stage_state.Status # "'IN_PROGRESS'"
        name = stage.Lane.LaneName if stage.Lane else 'Unknown'
        app_logger.info(f'Start Processing Stage: {name} - {stage_id} Status: {status}')
        if status == 'IN_PROGRESS' and name == 'Initial':
            pending_tasks = find_all_pending_tasks(stage_id)
            for task_instance in pending_tasks:
                if task_instance.TaskDef.TaskName == 'AssignNCRC':
                    _assign_role(task_instance.TaskInstanceId, 'NCRC', user, application_id)
                    print(f'  Assign Role: {task_instance.TaskDef.TaskName}')
                next_pending_tasks = find_all_pending_tasks(stage_id)
                while len(next_pending_tasks) > 0:
                    for next_task_instance in next_pending_tasks:
                        complete_task(next_task_instance)
                        completed_tasks.append(next_task_instance.TaskInstanceId)
                        #process_task_flow(next_task_instance, stage_id, completed_tasks)
                        next_pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'NDA':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0:
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Inspection':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0:
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Ingredients':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0:
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Products':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0:
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Contract':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0:
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

        elif status == 'IN_PROGRESS' and name == 'Certification':
            pending_tasks = find_all_pending_tasks(stage_id)
            while len(pending_tasks) > 0:
                for task_instance in pending_tasks:
                    print(f'  Completing Task: {task_instance.TaskDef.TaskName}')
                    complete_task(task_instance)
                    completed_tasks.append(task_instance.TaskInstanceId)
                    pending_tasks = find_all_pending_tasks(stage_id)

    stage_list = find_all_stages_for_process(process_id)
    for stage in stage_list:
        print(f'Stage {stage.Lane.LaneName} Status {stage.Status}')
    print(f"Workflow for application {application_id} completed {completed_tasks}.")
    app_logger.info(f"Workflow for application {application_id} completed {completed_tasks}.")

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

def do_cleanup(application_id, process_id):
    session.execute(text(f"""
        DELETE FROM TaskComments where [ProcessInstanceId] = {process_id};
        DELETE FROM WorkflowHistory where [InstanceId] = {process_id};
      
    """))
    session.commit()
    stage_list = find_all_stages_for_process(process_id)
    for stage in stage_list:
        session.execute(text(f"""
            DELETE FROM TaskInstances where StageId = {stage.StageInstanceId};
        """))
        session.commit()
        session.execute(text(f"""
            DELETE FROM StageInstance where StageInstanceId = {stage.StageInstanceId};
        """))
        session.commit()
    session.execute(text(f"""
        DELETE from RoleAssigment where ApplicationId = {application_id};
        DELETE FROM ProcessInstances where ApplicationId = {application_id};
        DELETE FROM WF_Applications where ApplicationId = {application_id};
       
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