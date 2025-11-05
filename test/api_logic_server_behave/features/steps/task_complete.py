"""
 Scenario: Complete Transaction Processing
     Given Start Task
      When Complete Task Called
      Then Next Task is PENDING
"""
from urllib import response
from behave import *
import requests, pdb
import test_utils
import json
import database.models as models
from datetime import datetime

start_task_id = 96
# Implement Behave Tests -- your code goes here

@given('Start Task')
def step_impl(context):
    run_workflow_to_completion()
    response = test_utils.get(f'http://192.168.13.131:5656/api/TaskInstance/{start_task_id}')
    assert response.status_code == 200
    task_instance = json.loads(response.text)['data']['attributes']
    assert task_instance is not None
    assert task_instance["Status"] in ['NEW','PENDING']
    context.task_instance = task_instance

@when('Complete Task Called')
def step_impl(context):
    task_instance = context.task_instance
    assert task_instance is not None
    #from api.api_discovery.ncrc_workflow import _complete_task
    url = f'http://192.168.13.131:5656/complete_task'
    '''
        task_instance_id = data.get("taskId")
        completed_by = data.get("completed_by",'system')
        completion_notes = data.get("completion_notes",'testing')
    '''
    result = test_utils.post(url, {'task_instance_id': task_instance["TaskInstanceId"], 'completed_by': 'admin', 'completion_notes': 'Task Completed by admin'})
    assert result.status_code == 200

@then('Next Task is PENDING')
def step_impl(context):
    scenario = "Complete Transaction Processing"
    test_utils.prt(f'Rules Report', scenario)
    response = test_utils.get(f'http://192.168.13.131:5656/api/TaskInstance/{start_task_id + 1}')
    assert response.status_code == 200
    next_task = json.loads(response.text)['data']['attributes']
    assert next_task['Status'] == 'PENDING'
    

def create_new_application():
    app = {
        "data": {
        "attributes": {
            "Name": "New Application",
            "Description": "Description of the new application",
            "Status": "NEW",
            "CompanyID": 11371556,  
            "PlantID": 14055823,
            "SubmissionDate": datetime.now().isoformat(),
            "CreatedBy": "tband",
            "CreatedDate": datetime.now().isoformat(),  
            "Priority": "HIGH",
            "ApplicationNumber": 564,
        },
        "type": "WFApplication"
        }
    }
    url = f'http://192.168.13.31:5656/api/WFApplication'
    response = test_utils.post(url, data=app)
    assert response.status_code == 201
    return response.json()['data']['id']

def start_workflow(application_id):
    url = f'http://192.168.13.31:5656/start_workflow'
    body = \
        {
            "process_name": "OU Application Init",
            "application_id": application_id,
            "started_by": "tband",
            "priority": "HIGH"
        }
    response = test_utils.post(url, data=body)
    assert response.status_code == 200
    return response.json()['data']['process_instance_id']


def find_all_stages_for_process(process_id):
    url = f'http://192.168.13.31:5656/api/StageInstance?filter[ProcessInstanceId]={process_id}'
    response = test_utils.get(url)
    assert response.status_code == 200
    return [data['id'] for data in response.json()['data']]

def find_all_pending_tasks(stage_list: list):
    pending_tasks = []
    for stage_id in stage_list:
        url = f'http://192.168.13.31:5656/api/TaskInstance?filter[StageId]={stage_id}&filter[Status]=PENDING' # {"name":"AssigneeRole","op": "ne","val": "SYSTEM"}'
        response = test_utils.get(url)
        assert response.status_code == 200
        pending_tasks.extend([data['id'] for data in response.json()['data']])
    for task_instance_id in pending_tasks:
        task_instance = test_utils.get(f'http://192.168.13.31:5656/api/TaskInstance/{task_instance_id}').json()['data']["attributes"]
        taskDef = test_utils.get(f'http://192.168.13.31:5656/api/TaskDefinition/{task_instance["TaskId"]}').json()['data']["attributes"] if task_instance else None
        task_name = taskDef["TaskName"] if taskDef else 'Unknown'
        if task_instance and taskDef and taskDef["AssigneeRole"] == 'SYSTEM':
            print(f'Skipping System Task {task_name} - {task_instance_id}')
            pending_tasks.remove(task_instance_id)
    return pending_tasks

def complete_task(task_instance_id):
    url = f'http://192.168.13.31:5656/complete_task'
    body  = \
    {
         "task_instance_id": task_instance_id,
         "result": "NO",
         "completed_by": "tband",
         "completion_notes": "Task completed successfully"

    }
    response = test_utils.post(url, data=body)
    assert response.status_code == 200

def run_workflow_to_completion():
    application_id = create_new_application()
    process_id = start_workflow(application_id)
    stages_list = find_all_stages_for_process(process_id)
    pending_tasks = find_all_pending_tasks(stages_list)
    completed_tasks = []
    while pending_tasks:
        for task_instance_id in pending_tasks:
            #task_instance = test_utils.get(f'http://192.168.13.31:5656/api/TaskInstance/{task_instance_id}').json()['data']["attributes"]
            #taskDef = test_utils.get(f'http://192.168.13.31:5656/api/TaskDefinition/{task_instance["TaskId"]}').json()['data']["attributes"] if task_instance else None
            #task_name = taskDef["TaskName"] if taskDef else 'Unknown'
            #if task_instance and taskDef and taskDef["AssigneeRole"] == 'SYSTEM':
            #    print(f'Skipping System Task {task_name} - {task_instance_id}')
            #    continue
    
            #print(f'Completing Task {task_name} - {task_instance_id}')
            if task_instance_id not in completed_tasks:
                complete_task(task_instance_id)
                completed_tasks.append(task_instance_id)
        pending_tasks = find_all_pending_tasks(stages_list)
    print(f"Workflow for application {application_id} completed.")
    #do_cleanup(application_id, process_id, stages_list)
    '''
            use dashboard;
        GO

        DELETE from RoleAssigment;
        DELETE FROM TaskComments;
        DELETE FROM WorkflowHistory;
        DELETE FROM TaskInstances;
        DELETE FROM StageInstance;
        DELETE FROM ProcessInstances;

    '''