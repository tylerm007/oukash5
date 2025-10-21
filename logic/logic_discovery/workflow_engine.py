from datetime import datetime
from database.models import TaskDefinition, TaskInstance
from integration.workflow import python_engine
from flask import app, request, jsonify, session
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
from config.config import Args
from flask import g
from dotmap import DotMap

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session

def get_client_uri() -> str:
    args = Args.instance
    content =  '{http_type}://{swagger_host}:{port}'
    if args.client_uri is not None:
        content = content.replace(
            '{http_type}://{swagger_host}:{port}',
            args.client_uri
        )
        content = content.replace("{api}", args.api_prefix[1:])
    else:
        content = content.replace("{http_type}", args.http_scheme)
        content = content.replace("{swagger_host}", args.swagger_host)
        content = content.replace("{port}", str(args.swagger_port))  # note - codespaces requires 443 here (typically via args)
        content = content.replace("{api}", args.api_prefix[1:])
    return content

def process_task_instance(task_instance: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    new_task_instance = models.TaskInstance.query.filter_by(TaskInstanceId=task_instance.TaskInstanceId).first()
    if not new_task_instance:
        print({"success": False, "message": f"No TaskInstance found with TaskInstanceId {task_instance.TaskInstanceId}"})
        return

    try:
        if task_instance.Status == 'PENDING':
            new_task_instance.StartedDate = datetime.datetime.utcnow()
        elif task_instance.Status == 'COMPLETED':
            new_task_instance.CompletedDate = datetime.datetime.utcnow()
        session.add(new_task_instance)
        #session.commit() # Cannot commit here, will be done by LogicRow commit
        update_next_task(new_task_instance, old_row, logic_row)
        logic_row.log(f"Next TaskInstance {new_task_instance.TaskInstanceId} ({new_task_instance.TaskDef.TaskName} processed.")
       
    except Exception as e:
        #session.rollback()
        app_logger.error(f"Error processing TaskInstance {new_task_instance}: {e}")
        #print({"success": False, "message": f"Error processing TaskInstance {new_task_instance}: {e}"})
        return
    
def create_invoice(task_instance_id, data: DotMap):
    ''' Create an EventAction for the given TaskInstanceId and EventKey
    '''
    task_instance = models.TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
    if not task_instance:
        data.Result = False
        data.ErrorMessage = f"No TaskInstance found with TaskInstanceId {task_instance_id}"
        return data

    from api.api_discovery.event_action import _create_invoice_fee
    fee =  float(data.Result) if 'Result' in data else 0.0
    application_id = task_instance.Stage.ProcessInstance.ApplicationId
    application = models.WFApplication.query.filter_by(ApplicationID=application_id).first()    
    company_id = application.CompanyID
    invoice_fee = _create_invoice_fee(company_id, fee)
    if not invoice_fee:
        data.ErrorMessage = f"Failed to create invoice fee for TaskInstanceId {task_instance_id}"
        data.Result = False
        return data
    event_key = f"INVOICE_{invoice_fee.INVOICE_ID}"
    from api.api_discovery.event_action import _create_event
    _create_event(task_instance_id, event_key)
    data.ResultData = {"EventKey": event_key}
    app_logger.info(f"EventAction created for TaskInstanceId {task_instance_id} with EventKey {event_key}")
    data.Result = True
    return data

def set_application_attribute(application_id, name, value, data: DotMap) -> DotMap:
    ''' Set an attribute of the WFApplication to a new value
        The simple setattr does not work and we cannot commit()
        will try PATCH
    '''
    application = get_application(application_id)
    if not application:
        data.Result = False
        data.ErrorMessage = f"No application found with ApplicationID {application_id}"
        return data
    if application[0]["Status"] == 'WTH':
        data.Result = False
        data.ErrorMessage = f"Cannot modify application {application_id} because it is Withdrawn (WTH)"
        return data
    payload = {
        "data": {
            "attributes": {
                f"{name}": f"{value}"
            },
            "type": "WFApplication",
            "id": f"{application_id}"
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    if data.access_token:
        headers['Authorization'] = data.access_token

    server_uri = get_client_uri()
    response = requests.patch(f"{server_uri}/api/WFApplication/{application_id}", json=payload, headers=headers)
    if response.status_code == 200:
        app_logger.info(f"Application {application_id} attribute {name} set to {value}")
        data.Result = True
        data.Message = f"Application {application_id} attribute {name} set to {value}"
    else:
        data.Result = False
        data.ErrorMessage = f"Application {application_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}"
        app_logger.error(f"Application {application_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
    return data

def set_task_attribute(task_instance_id, name, value, data: DotMap) -> bool:
    ''' Set an attribute of the TaskInstance to a new value
        The simple setattr does not work and we cannot commit()
        will try PATCH
    '''
    payload = {
        "data": {
            "attributes": {
                f"{name}": f"{value}"
            },
            "type": "TaskInstance",
            "id": f"{task_instance_id}"
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    if data.access_token:
        headers['Authorization'] = data.access_token
   
    server_uri = get_client_uri()
    response = requests.patch(f"{server_uri}/api/TaskInstance/{task_instance_id}", json=payload, headers=headers)
    if response.status_code == 200:
        app_logger.info(f"TaskInstance {task_instance_id} attribute {name} set to {value}")
        data.Result = True
        data.Message = f"TaskInstance {task_instance_id} attribute {name} set to {value}"
    else:
        data.Result = False
        data.ErrorMessage = f"TaskInstance {task_instance_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}"
        app_logger.error(f"TaskInstance {task_instance_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
    return data


def set_stage_attribute(stage_id, name, value, data:DotMap) -> DotMap:
    ''' Set an attribute of the StageInstance to a new value
        The simple setattr does not work and we cannot commit()
        will try PATCH
    '''
    payload = {
        "data": {
            "attributes": {
                f"{name}": f"{value}"
            },
            "type": "StageInstance",
            "id": f"{stage_id}"
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    if data.access_token:
        headers['Authorization'] = data.access_token
    
    server_uri = get_client_uri()
    response = requests.patch(f"{server_uri}/api/StageInstance/{stage_id}", json=payload, headers=headers)
    if response.status_code == 200:
        app_logger.info(f"StageInstance {stage_id} attribute {name} set to {value}")
        data.Result = True
        data.Message = f"StageInstance {stage_id} attribute {name} set to {value}"
    else:
        data.Result = False
        data.ErrorMessage = f"StageInstance {stage_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}"
        app_logger.error(f"StageInstance {stage_id} attribute {name} set to {value} \ncode: {response.status_code} message: {response.text}")
    return data


def get_application(application_id):
    application = models.WFApplication.query.filter_by(ApplicationID=application_id).first()
    if not application:
        return None, jsonify({"success": False, "message": f"No application found with ApplicationID {application_id}"}), 404
    return application.to_dict(), None, None

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
            logic_row.log(f"Cannot proceed with task {taskDef.TaskName} because dependency task {from_task_instance.TaskInstanceId} is not COMPLETED.")
            return False
    return True

def test_complete_task(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    '''
        This is a constraint - it only tests if the update is valid.
        Test if a TaskInstance can be COMPLETED based on its dependencies.
    '''
    if logic_row.ins_upd_dlt == 'upd' and row.Status == 'COMPLETED' and old_row.Status in ['NEW', 'PENDING']:
        task_def = row.TaskDef
        if not task_def:
            logic_row.log(f"No task definition found for  {row.TaskDef.TaskName}  TaskId {row.TaskId} in test_complete_task")
            return False
        is_valid = validate_prior_tasks(task_def, row.StageId, logic_row)
        if not is_valid:
            logic_row.log(f"Cannot complete task: {row.TaskDef.TaskName} id:{row.TaskInstanceId} due to unmet dependencies not COMPLETED.")
            return False
        return True  # Only allow setting to Pending from COMPLETED
    elif logic_row.ins_upd_dlt == 'upd' and old_row.Status == 'COMPLETED' and row.Status != 'COMPLETED':
        logic_row.log(f"Task  {row.TaskDef.TaskName}  ID: {row.TaskInstanceId} was COMPLETED and is now being changed to {row.Status}.")
        # If a task is reverted from COMPLETED to another status, we might want to handle that
        # For simplicity, we allow it here but in a real scenario, you might want to enforce rules
        # such as reverting dependent tasks as well.
        
    return True

def update_next_task(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    '''
    When a task is COMPLETED, update the next tasks in the workflow to be 'PENDING' ready to start.
    '''
    if logic_row.ins_upd_dlt == 'upd' and row.Status in ['PENDING'] and old_row.Status != row.Status:
        row.StartedDate = datetime.datetime.utcnow()
    if logic_row.ins_upd_dlt == 'upd' and row.Status in ['PENDING', 'COMPLETED'] and old_row and old_row.Status != row.Status:
    # only proceed if the task instance Status was updated and is now PENDING or COMPLETED
        task_id = row.TaskInstanceId
        task_def = row.TaskDef
        if not task_def:
            logic_row.log(f"No task definition found for  {row.TaskDef.TaskName}  TaskId {row.TaskId} in update_next_task")
            return
        

        if task_def.TaskType in ['START', 'END', 'GATEWAY', 'SUBPROCESS'] and row.Status != 'COMPLETED':
            logic_row.log(f"Task  {task_def.TaskName}  ID: {task_id} with status {row.Status} is of type {task_def.TaskType} and AutoComplete: {row.TaskDef.AutoComplete}.")
            if task_def.AutoComplete:
                logic_row.log(f"Task {task_id} is auto-completing.")
                row.Status = 'COMPLETED'
                logic_row.log(f'Task {task_def.TaskName} TaskInstance {task_id} AutoComplete=True.')
        
        logic_row.log(f'TaskInstance {task_id} Status:{row.Status}. Checking for next tasks to set to Pending.')
        task_flow = task_def.TaskFlowList or []
        for task_flow in task_flow:
            next_task_def = task_flow.ToTaskId
            next_task_instance = models.TaskInstance.query.filter_by(TaskId=next_task_def, StageId=row.StageId).first()
            if next_task_instance and next_task_instance.Status in ['NEW', 'PENDING']:
                if next_task_instance.TaskDef.AutoComplete and validate_prior_tasks(next_task_instance.TaskDef, row.StageId, logic_row):
                    next_task_instance.Status = 'COMPLETED'
                    logic_row.log(f'Next task {next_task_instance.TaskDef.TaskName} ID: {next_task_instance.TaskInstanceId} auto-completed due to AutoComplete=True and all dependencies met.')
                    future_task = next_task_instance.TaskDef.TaskFlowList or []
                    for future_flow in future_task: 
                        future_task_def = future_flow.ToTaskId
                        future_task_instance = models.TaskInstance.query.filter_by(TaskId=future_task_def, StageId=row.StageId).first()
                        if future_task_instance and future_task_instance.Status in ['NEW']:
                            if validate_prior_tasks(future_task_instance.TaskDef, row.StageId, logic_row):
                                if future_task_instance.TaskDef.AutoComplete:
                                    future_task_instance.Status = 'COMPLETED'
                                    future_task_instance.CompletedDate = datetime.datetime.utcnow()
                                    logic_row.log(f'Future task {future_task_instance.TaskInstanceId} auto-completed due to AutoComplete=True and all dependencies met.')
                                    update_next_task(future_task_instance, row, logic_row)  # recursively update next tasks
                                else:
                                    future_task_instance.Status = 'PENDING'
                                    future_task_instance.StartedDate = datetime.datetime.utcnow()
                                    logic_row.log(f'Future task {future_task_instance.TaskInstanceId} set to PENDING as all dependencies are COMPLETED.')
                elif next_task_instance.TaskDef.TaskType == 'START':
                    next_task_instance.Status = 'COMPLETED'
                    logic_row.log(f'Next task {next_task_instance.TaskInstanceId} auto-completed because it is a START task.')
                elif next_task_instance.TaskDef.TaskType in ['END'] and  row.TaskDef.TaskType != 'CONDITION':
                    next_task_instance.Status = 'COMPLETED'
                    logic_row.log(f'Next task {next_task_instance.TaskInstanceId} auto-completed because it is an {next_task_instance.TaskDef.TaskCategory} task.')
                elif next_task_instance.TaskDef.TaskType in ['GATEWAY']:
                    # A GATEWAY task can be set to PENDING if all its from dependencies are COMPLETED
                    if validate_prior_tasks(next_task_instance.TaskDef, row.StageId, logic_row):
                        next_task_instance.Status = 'PENDING' if next_task_instance.AutoComplete else 'COMPLETED'
                        logic_row.log(f'Next GATEWAY task {next_task_instance.TaskInstanceId} set to PENDING as all dependencies are COMPLETED.')
                        if next_task_instance.AutoComplete:
                            update_next_task(next_task_instance, row, logic_row)  # recursively update next tasks
                elif row.TaskDef.TaskType == 'CONDITION' and row.Status == 'COMPLETED':
                    result = row.Result or None
                    condition = task_flow.Condition or ""
                    if result and condition.lower() == result.lower():
                        next_task_instance.Status = 'PENDING'
                        logic_row.log(f'Next CONDITION task {next_task_instance.TaskInstanceId} set to PENDING based on condition.')
                else:
                    next_task_instance.Status = 'PENDING'
                    next_task_instance.StartedDate = datetime.datetime.utcnow()
            elif row.Status == 'COMPLETED' and next_task_instance and next_task_instance.Status == 'NEW':
                next_task_instance.Status = 'PENDING'
                next_task_instance.StartedDate = datetime.datetime.utcnow()
                logic_row.log(f'Next task {next_task_instance.TaskDef.TaskName} ID: {next_task_instance.TaskInstanceId} is NEW, cannot set to PENDING until dependencies are met.')
            if row.Status == 'PENDING' and row.StartedDate is None:
                row.StartedDate = datetime.datetime.utcnow()
            elif row.Status == 'COMPLETED' and row.CompletedDate is None:
                row.CompletedDate = datetime.datetime.utcnow()
            logic_row.log(f'Next Task {next_task_instance.TaskDef.TaskName} Type:{next_task_instance.TaskDef.TaskType} ID: {next_task_instance.TaskInstanceId} set to {next_task_instance.Status}')
            #logic_row.update(reason=f"Update next task status to {next_task_instance.Status}", row=next_task_instance)
            process_task_instance(next_task_instance, old_row, logic_row)
            
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
        row.Result = call_script_engine(row, old_row, logic_row, script)
        logic_row.log(f'PostScriptJson Result: {row.Result}')
        #TODO add WF task history info

def call_script_engine(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow, script: str):

    if logic_row.ins_upd_dlt == 'upd':  
        task_id = row.TaskInstanceId
        stage_id = row.StageId
        if row:
            # NOTE: we want to cascade the ResultData to subsequent tasks
            # depending on the workflow requirements
            task_def = row.TaskDef
            parent_instances = task_def.ToTaskTaskFlowList or [] # row.ParentInstance TODO
            if parent_instances:
                for parent in parent_instances:
                    if parent:
                        #and parent.ResultData:
                        parent_instance = models.TaskInstance.query.filter_by(TaskId=parent.FromTaskId, StageId=stage_id).first()
                        result_data = parent_instance.ResultData if "ResultData" in dir(parent_instance) else {}
                        if result_data:
                            row.ResultData.update(result_data)
                            logic_row.log(f'Inheriting ResultData from parent task {parent_instance.TaskInstanceId}')
                            row.ResultData.update(result_data)
            # collect prior context from dependent tasks and create a union of ResultData
            application_id = row.Stage.ProcessInstance.ApplicationId
            se = python_engine.PythonScriptEngine()
            data = row.ResultData or {}
            task = row.to_dict()

            access_token = request.headers.get("Authorization")
            # Get current state to use in script calls
            context = {"data": data,"application_id": application_id, "task": task, "task_id": task_id}
            external_context = {"get_application": get_application, "set_application_attribute":set_application_attribute,"access_token": access_token,"set_task_attribute":set_task_attribute,
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

def call_task_script_engine(row: models.TaskInstance, access_token:str, parent_instance: models.TaskInstance = None):
    task_id = row.TaskInstanceId
    task_instance_id = task_id
    stage_id = row.StageId
    task_def = row.TaskDef
    script = task_def.PostScriptJson or None
    if not script or script == '':
        return None
    if parent_instance:
        result_data = parent_instance.ResultData if "ResultData" in dir(parent_instance) else {}
        if result_data:
            row.ResultData.update(result_data)
            app_logger.info(f'Inheriting ResultData from parent task {parent_instance.TaskInstanceId}')
            
    # collect prior context from dependent tasks and create a union of ResultData
    application_id = row.Stage.ProcessInstance.ApplicationId
    se = python_engine.PythonScriptEngine()
    data = DotMap({})
    data.access_token = access_token
    task = DotMap(row.to_dict())
    # Get current state to use in script calls
    data.Result = task.Result
    data.ResultData = task.ResultData   
    data.application_id = application_id
    data.task_instance_id = task_instance_id
    data.stage_id = stage_id
    context = {"data": data,"application_id": application_id, "task": task, "task_instance_id": task_instance_id, "task_id": task_id, "stage_id": stage_id,"access_token": access_token}
    external_context = {"get_application": get_application,
                        "set_application_attribute":set_application_attribute,
                        "set_stage_attribute":set_stage_attribute,     
                        "set_task_attribute":set_task_attribute,
                        "create_invoice":create_invoice,
                        "models":models,
                        "app_logger":app_logger,
                        "datetime":datetime,
                        "Decimal":Decimal}
    try:
        r = se.execute(script=script, task=context, external_context=external_context)
        if r:
            data = r.get('data', None)
            app_logger.info(f'Script executed successfully for task_id {task_id}')
            app_logger.info(f'Script execution Result: {data}')
            return data
    except Exception as e:
        app_logger.error(f'Error executing script for task_id {task_id}: {e}')
        return None
    
def declare_logic():
    pass
    # A TaskInstance can only be set to 'Pending' if all its from dependencies are 'COMPLETED'
    # A TaskInstance can only be set to 'COMPLETED' if it is currently 'Pending'

    # A TaskInstance with TaskCategory 'START' can always be set to 'COMPLETED' 
    #Rule.constraint(validate=models.TaskInstance, calling=test_complete_task, error_msg="Cannot complete this task due to unmet dependencies not COMPLETED.")
    
    # TaskInstance PreScriptJson and PostScriptJson execution are called before and after row update
    # they set the Result and ResultData fields respectively with context data
    #Rule.row_event(on_class=models.TaskInstance,calling=update_next_task)
    #Rule.after_flush_row_event(on_class=models.TaskInstance, calling=call_script_engine_post)