from os import access
from urllib import response
from database.models import StageInstance, WFApplication, TaskInstance, TaskDefinition, ProcessInstance
import database.models as models
from flask import request, jsonify
import requests
import logging
import safrs
from sqlalchemy.sql import text

db = safrs.DB 
session = db.session

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass

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

    @app.route('/run_workflow_to_completion', methods=['GET','OPTIONS'])
    def run_workflow_to_completion_endpoint():
        run_workflow_to_completion()
        return jsonify({"result": f'Workflow run to completion'})

    @app.route('/reset_task_instances/<application_id>', methods=['GET','OPTIONS'])
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

    @app.route('/cleanup_workflow_data/<application_id>/<process_id>', methods=['GET','OPTIONS'])
    def cleanup_workflow_data(application_id, process_id):
        # Implement cleanup logic here
        do_cleanup(application_id, process_id)
        return jsonify({"result": f'Cleanup initiated for Application ID: {application_id}, Process ID: {process_id}'})

def create_new_application():
    from datetime import datetime
    application = WFApplication(
            Name="New Application",
            Description="Description of the new application",
            Status="NEW",
            CompanyID=11371556,
            PlantID=14055823,
            SubmissionDate=datetime.now().isoformat(),
            CreatedBy="tband",
            CreatedDate=datetime.now().isoformat(),
            Priority="HIGH",
            ApplicationNumber=564,
            WFDashboardID=1
    )
    session.add(application)
    session.commit()
    return application.ApplicationID


def start_workflow(application_id):
    from api.api_discovery.start_workflow import _start_workflow
   
    process_name = "OU Application Init"
    application_id = application_id
    started_by = "tband"
    priority = "HIGH"

    response = _start_workflow(process_name, int(application_id), started_by, priority)
    return response['process_instance_id']


def find_all_stages_for_process(process_id):
    stages = StageInstance.query.filter(StageInstance.ProcessInstanceId == process_id).all()
    return [stage.StageInstanceId for stage in stages]

def find_all_pending_tasks(stage_list: list):
    pending_tasks = []
    for stage_id in stage_list:
        response = session.query(models.TaskInstance).filter(models.TaskInstance.StageId == stage_id, models.TaskInstance.Status == 'PENDING').all()
        pending_tasks.extend([task for task in response])
    for task_instance in pending_tasks:
        taskDef = task_instance.TaskDef
        task_name = taskDef.TaskName if taskDef else 'Unknown'
        if task_instance and taskDef and taskDef.AssigneeRole == 'SYSTEM':
            print(f'Skipping System Task {task_name} - {task_instance}')
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
    result = 'NO' if "Withdraw" in task_name else None
    response = _complete_task(task_instance_id=task_instance_id, result=result, completed_by='tband', completion_notes='Task completed successfully', access_token=access_token, depth=0)
    app_logger.info(f'TaskInstance completed: {task_instance_id} {response}')

def run_workflow_to_completion():
    application_id = create_new_application()
    process_id = start_workflow(application_id)
    stages_list = find_all_stages_for_process(process_id)
    pending_tasks = find_all_pending_tasks(stages_list)
    completed_tasks = []
    for task_instance in pending_tasks:
        print(f'Completing TaskInstance: {task_instance.TaskDef.TaskName}')
        complete_task(task_instance)
        completed_tasks.append(task_instance.TaskInstanceId)
        process_task_flow(task_instance, completed_tasks)
       
    print(f"Workflow for application {application_id} completed {completed_tasks}.")
def process_task_flow(task_instance, completed_tasks):
    task_flow_instances = find_task_flow(task_instance)
    for task_flow in task_flow_instances:
        next_task_def = session.query(models.TaskDefinition).filter(models.TaskDefinition.TaskId == task_flow.ToTaskId).first()
        if next_task_def and next_task_def.AssigneeRole != 'SYSTEM' and task_instance.Status == 'COMPLETED':
            next_task_instance = session.query(models.TaskInstance).filter(models.TaskInstance.TaskId == next_task_def.TaskId, models.TaskInstance.StageId == task_instance['StageId']).first()
            if next_task_instance and next_task_instance.Status in ['NEW','PENDING'] and next_task_instance.TaskInstanceId not in completed_tasks:
                print(f'  Next Task to complete: {next_task_def.TaskName}')
                complete_task(next_task_instance)
                completed_tasks.append(next_task_instance.TaskInstanceId)
                process_task_flow(next_task_instance, completed_tasks)

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
    stage_list = find_all_stages_for_process(process_id)
    for stage_id in stage_list:
        session.execute(text(f"""
            DELETE FROM TaskInstances where StageId = {stage_id};
            DELETE FROM StageInstance where StageInstanceId = {stage_id};
           
        """))
    session.execute(text(f"""
        DELETE from RoleAssigment where ApplicationId = {application_id};
        DELETE FROM ProcessInstances where ApplicationId = {application_id};
        DELETE FROM WFApplication where ApplicationId = {application_id};
       
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