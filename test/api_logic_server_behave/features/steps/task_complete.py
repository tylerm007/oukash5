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
    response = test_utils.get(f'http://localhost:5656/api/TaskInstance/{start_task_id}')
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
    url = f'http://localhost:5656/complete_task'
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
    response = test_utils.get(f'http://localhost:5656/api/TaskInstance/{start_task_id + 1}')
    assert response.status_code == 200
    next_task = json.loads(response.text)['data']['attributes']
    assert next_task['Status'] == 'PENDING'