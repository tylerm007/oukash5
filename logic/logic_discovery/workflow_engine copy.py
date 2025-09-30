from datetime import datetime
from anyio import TASK_STATUS_IGNORED
from config import activate_logicbank
from database.models import TaskDefinition, TaskInstance
from integration.workflow import python_engine
from flask import app, request, jsonify, session
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
import logging
import safrs
from config.config import Args
from config.config import Config
import datetime, os
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from logic_bank.logic_bank import DeclareRule
import database.models as models
import requests
import config.config as config

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session

def process_task_instance(task_instance: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    # 
    #new_task_instance = models.TaskInstance.query.filter_by(TaskInstanceId=task_instance.TaskInstanceId).first()
    if not task_instance:
        logic_row.log({ f"Unable to process - No TaskInstance found with TaskInstanceId {task_instance.TaskInstanceId}"})
        return

    task_def = task_instance.TaskDef
    if task_def is None:
        logic_row.log(f"No TaskDefinition found for TaskInstanceId {task_instance.TaskInstanceId}")
        return

    #update_task_history (task_instance, old_row, logic_row)
    task_flow = task_def.TaskFlowList or []
    for task_flow in task_flow:
        next_task_def = task_flow.ToTaskId
        next_task_instance = models.TaskInstance.query.filter_by(TaskId=next_task_def, StageId=task_instance.StageId).first()
        next_task_status = next_task_instance.Status if next_task_instance else 'N/A'
        update_future_tasks(next_task_instance, next_task_instance, logic_row)
        if next_task_instance.Status != next_task_status:
            update_task_instance(next_task_instance)
            logic_row.log(f"TaskInstance {task_instance.TaskDef.TaskName} Next TaskInstance ({next_task_instance.TaskDef.TaskName}) processed.")
            if next_task_instance.Status == 'COMPLETED':
                call_script_engine_post(next_task_instance, task_instance, logic_row)

def update_future_tasks(next_task_instance: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    # only sent future state if prior state is Valid (Completed)
    if next_task_instance and next_task_instance.Status in ['NEW','PENDING'] and validate_prior_tasks(next_task_instance.TaskDef, next_task_instance.StageId, logic_row):
        if next_task_instance.TaskDef.AutoComplete and next_task_instance.Status != 'COMPLETED':
            next_task_instance.Status = 'COMPLETED'
            if next_task_instance.CompletedDate is None:
                next_task_instance.CompletedDate = datetime.datetime.utcnow()
            process_task_instance(next_task_instance, old_row, logic_row)
        elif next_task_instance.Status == 'NEW':
            next_task_instance.Status = 'PENDING'
            if next_task_instance.CompletedDate is None:
                next_task_instance.CompletedDate = datetime.datetime.utcnow()


def set_application_attribute(application_id, name, value) -> bool:
    ''' Set an attribute of the WFApplication to a new value
        The simple setattr does not work and we cannot commit()
        will try PATCH
    '''
    data = {
        "data": {
            "attributes": {
                f"{name}": f"{value}"
            },
            "type": "WFApplication",
            "id": f"{application_id}"
        }
    }
    autorization = request.headers.get('Authorization', None)
    headers = {
        'Content-Type': 'application/json'
    }
    if autorization:
        headers['Authorization'] = autorization
    
    args = config.Args
    server = args.swagger_host
    port = args.port
    server_uri = "http://localhost:5656" #f"http://{server}:{port}"
    response = requests.patch(f"{server_uri}/api/WFApplication/{application_id}", json=data, headers=headers)
    if response.status_code == 200:
        app_logger.info(f"Application {application_id} attribute {name} set to {value}")
        return True
    app_logger.error(f"Application {application_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
    return False

def update_task_instance(task_instance: models.TaskInstance):
    try:
        task_instance_id = task_instance.TaskInstanceId
        data = {
        "data": {
            "attributes": task_instance.to_dict(),
            "type": "TaskInstance",
            "id": f"{task_instance_id}"
        }
        }
        autorization = request.headers.get('Authorization', None)
        headers = {
            'Content-Type': 'application/json'
        }
        if autorization:
            headers['Authorization'] = autorization
    
        args = config.Args
        server = args.swagger_host
        port = args.port
        server_uri = "http://localhost:5656" #f"http://{server}:{port}"
        response = requests.patch(f"{server_uri}/api/TaskInstance/{task_instance_id}", json=data, headers=headers)
        if response.status_code == 200:
            app_logger.info(f"TaskInstance {task_instance} updated to Status {task_instance.Status}")
            wf_activity = models.WFActivityLog(
                ApplicationID=task_instance.Stage.ProcessInstance.ApplicationId,
                ActivityType=f"TaskInstance '{task_instance.TaskDef.TaskName}' Updated to {task_instance.Status}",
                TaskInstanceId=task_instance_id,
                Status=task_instance.Status,
                Category = task_instance.TaskDef.TaskCategory if task_instance.TaskDef else 'N/A',
                ActivateDate=datetime.datetime.utcnow(),
                UserName = "system"
            )   
            data = {"data": {
                "attributes": wf_activity.to_dict(),
                "type": "WFActivityLog"
            }}
            response = requests.post(f"{server_uri}/api/WFActivityLog", json=data, headers=headers)
            return True
        else:
            app_logger.error(f"TaskInstance {task_instance_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
            return False

    except Exception as e:
        app_logger.error(f"TaskInstance {task_instance_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
        return False

def set_task_attribute(task_instance_id, name, value) -> bool:
    ''' Set an attribute of the TaskInstance to a new value
        The simple setattr does not work and we cannot commit()
        will try PATCH
    '''
    data = {
        "data": {
            "attributes": {
                f"{name}": f"{value}"
            },
            "type": "TaskInstance",
            "id": f"{task_instance_id}"
        }
    }
    autorization = request.headers.get('Authorization', None)
    headers = {
        'Content-Type': 'application/json'
    }
    if autorization:
        headers['Authorization'] = autorization
   
    args = config.Args
    server = args.swagger_host
    port = args.port
    server_uri = "http://localhost:5656" #f"http://{server}:{port}"
    response = requests.patch(f"{server_uri}/api/TaskInstance/{task_instance_id}", json=data, headers=headers)
    if response.status_code == 200:
        app_logger.info(f"TaskInstance {task_instance_id} attribute {name} set to {value}")
        return True
    app_logger.error(f"TaskInstance {task_instance_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
    return False


def set_stage_attribute(stage_id, name, value) -> bool:
    ''' Set an attribute of the StageInstance to a new value
        The simple setattr does not work and we cannot commit()
        will try PATCH
    '''
    data = {
        "data": {
            "attributes": {
                f"{name}": f"{value}"
            },
            "type": "StageInstance",
            "id": f"{stage_id}"
        }
    }
    autorization = request.headers.get('Authorization', None)
    headers = {
        'Content-Type': 'application/json'
    }
    if autorization:
        headers['Authorization'] = autorization

    args = config.Args
    server = args.swagger_host
    port = args.port
    server_uri = "http://localhost:5656" #f"http://{server}:{port}"
    response = requests.patch(f"{server_uri}/api/StageInstance/{stage_id}", json=data, headers=headers)
    if response.status_code == 200:
        app_logger.info(f"StageInstance {stage_id} attribute {name} set to {value}")
        return True
    app_logger.error(f"StageInstance {stage_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
    return False


def get_application(application_id):
    application = models.WFApplication.query.filter_by(ApplicationID=application_id).first()
    if not application:
        return None, jsonify({"success": False, "message": f"No application found with ApplicationID {application_id}"}), 404
    return application

def validate_prior_tasks(taskDef: TaskDefinition, stage_id: int, logic_row: LogicRow):
    '''
    Validate that all prior tasks in the workflow (TaskFlow)are completed before allowing this task to proceed.
    '''
    dependencies = taskDef.ToTaskTaskFlowList  # List of TaskFlow objects where this task is the ToTask
    if dependencies is None or len(dependencies) == 0:
        return True  # No dependencies, so it's valid to proceed
    for dependency in dependencies:
        from_task_def = dependency.FromTaskId
        from_task_instance = models.TaskInstance.query.filter_by(TaskId=from_task_def, StageId=stage_id).first()
        if from_task_instance and from_task_instance.Status != 'COMPLETED' and taskDef.TaskType not in ['START']:
            logic_row.log(f"Cannot proceed with task {taskDef.TaskName} because dependency task {from_task_instance.TaskDef.TaskName} Status was not COMPLETED.")
            return False
    return True

def test_complete_task(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    '''
        This is a constraint - it only tests if the update is valid.
        Test if a TaskInstance can be COMPLETED based on its dependencies.
    '''
    if logic_row.ins_upd_dlt == 'upd' and row.Status == 'COMPLETED' and old_row and old_row.Status in ['PENDING']:
        task_def = row.TaskDef
        if not task_def:
            logic_row.log(f"No task definition found for Task {row.TaskInstanceId} in test_complete_task")
            return False
        is_valid = validate_prior_tasks(task_def, row.StageId, logic_row)
        if not is_valid:
            logic_row.log(f"Cannot complete task: {row.TaskDef.TaskName} id: {row.TaskInstanceId} due to unmet dependencies not COMPLETED.")
            return False
        return True  # Only allow setting to Pending from COMPLETED
    elif logic_row.ins_upd_dlt == 'upd'  and row.Status != 'COMPLETED'and old_row and old_row.Status == 'COMPLETED':
        logic_row.log(f"Task  {row.TaskDef.TaskName}  ID: {row.TaskInstanceId} was COMPLETED and is now being changed to {row.Status}.")
        # If a task is reverted from COMPLETED to another status, we might want to handle that
        # For simplicity, we allow it here but in a real scenario, you might want to enforce rules
        # such as reverting dependent tasks as well.
        
    return True

def update_task_dates(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    '''
    Update the StartedDate and CompletedDate based on the Status changes.
    '''
    if logic_row.ins_upd_dlt == 'upd' and row.Status in ['NEW', 'PENDING', 'COMPLETED'] and old_row and old_row.Status != row.Status:
        task_id = row.TaskInstanceId
        task_def = row.TaskDef
        if not task_def:
            logic_row.log(f"No task definition found for TaskId {row.TaskInstanceId} in update_next_task")
            return
        if row.TaskDef.AutoComplete and row.Status != 'COMPLETED':
            row.Status = 'COMPLETED'
        if row.Status == 'COMPLETED' and row.CompletedDate is None:
            row.CompletedDate = datetime.datetime.utcnow()
            logic_row.log(f'Task {row.TaskDef.TaskName} TaskInstance {row.TaskInstanceId} marked as COMPLETED at {row.CompletedDate}.')
        elif row.Status == 'PENDING' and row.StartedDate is None:
            row.StartedDate = datetime.datetime.utcnow()
            logic_row.log(f'Task {row.TaskDef.TaskName} TaskInstance {row.TaskInstanceId} marked as PENDING at {row.StartedDate}.')
    return

def update_task(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    '''
    When a task is COMPLETED, update the next tasks in the workflow to be 'PENDING' ready to start.
    NEW Tasks are ignored (/start_workflow sets them to NEW)
    '''
    
    if logic_row.ins_upd_dlt == 'upd' and row.Status in ['PENDING', 'COMPLETED'] and old_row and old_row.Status != row.Status:
    # only proceed if the task instance Status was updated and is now PENDING or COMPLETED
        task_id = row.TaskInstanceId
        task_def = row.TaskDef
        if not task_def:
            logic_row.log(f"No task definition found for TaskId {row.TaskInstanceId} in update_next_task")
            return

        logic_row.log(f'TaskInstance {task_id} - {task_def.TaskName} Status: {row.Status}. Checking for next tasks to set to Pending.')
        process_task_instance(row, old_row, logic_row)
            
    return

def call_script_engine_pre(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    task_def = row.TaskDef
    script = task_def.PreScriptJson or ''
    #logic_row.log(f'PreScriptJson: {script}')
    # may want to restrict the content to Python only
    if script != '' and logic_row.ins_upd_dlt == 'upd' and row.Status == 'PENDING' and row.Status != old_row.Status:
        row.Result = call_script_engine(row, old_row, logic_row, script)
        logic_row.log(f'PreScriptJson Result: {row.Result}')

def call_script_engine_post(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    task_def = row.TaskDef
    script = task_def.PostScriptJson or ''
    logic_row.log(f'PostScriptJson: {script}')
    if script != '' and logic_row.ins_upd_dlt == 'upd' and row.Status == 'COMPLETED' and row.Status != old_row.Status:
        result_data = call_script_engine(row, old_row, logic_row, script)
        logic_row.log(f'PostScriptJson Result: {result_data}')
        set_task_attribute(row.TaskInstanceId, 'ResultData', result_data)

def call_script_engine(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow, script: str):

    if logic_row.ins_upd_dlt == 'upd':  
        task_id = row.TaskInstanceId
        if row:
            # NOTE: we want to cascade the ResultData to subsequent tasks
            # depending on the workflow requirements
            task_def = row.TaskDef
            parent_instances = None # row.ParentInstance TODO
            if parent_instances:
                for parent in parent_instances:
                    if parent and parent.ResultData:
                        logic_row.log(f'Inheriting ResultData from parent task {parent.TaskInstanceId}')
                        row.ResultData.update(parent.ResultData)
            # collect prior context from dependent tasks and create a union of ResultData
            application_id = row.Stage.ProcessInstance.ApplicationId
            se = python_engine.PythonScriptEngine()
            data = row.ResultData or {}
            task = row.to_dict()
            context = {"data": data,"application_id": application_id, "task": task, "task_id": task_id}
            external_context = {"get_application": get_application, "set_application_attribute":set_application_attribute, "set_task_attribute":set_task_attribute,
                                "models":models,"session":session,"db":db,"app_logger":app_logger,"Args":Args,"Config":Config,"datetime":datetime,"Decimal":Decimal,"logic_row": logic_row}
            r = se.execute(script=script, task=context, external_context=external_context)
            if r:
                result = r.get('data', None)
                app_logger.info(f'Script executed successfully for task_id {task_id}')
                row.ResultData = result
                logic_row.log(f'Script execution Result: {result}')
                return result

        else:
            app_logger.warning(f'No task found with task_id {task_id}') 

def declare_logic():
    pass
    # A TaskInstance can only be set to 'Pending' if all its from dependencies are 'COMPLETED'
    # A TaskInstance can only be set to 'COMPLETED' if it is currently 'Pending'

    # A TaskInstance with TaskCategory 'START' can always be set to 'COMPLETED' 
    #Rule.constraint(validate=models.TaskInstance, calling=test_complete_task, error_msg="Cannot complete this task due to unmet dependencies not COMPLETED.")
    
    # TaskInstance PreScriptJson and PostScriptJson execution are called before and after row update
    # they set the Result and ResultData fields respectively with context data
    #Rule.row_event(on_class=models.TaskInstance,calling=update_task_dates)
    #Rule.after_flush_row_event(on_class=models.TaskInstance, calling=call_script_engine_post)
    #Rule.after_flush_row_event(on_class=models.TaskInstance, calling=update_task)