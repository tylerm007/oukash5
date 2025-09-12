from datetime import datetime
from math import log
from operator import call
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

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session

def get_application(application_id):
    application = models.WFApplication.query.filter_by(ApplicationID=application_id).first()
    if not application:
        return None, jsonify({"success": False, "message": f"No application found with ApplicationID {application_id}"}), 404
    return application

def test_complete_task(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    '''
    Test if a task can be completed based on its dependencies.
    '''
    if logic_row.ins_upd_dlt == 'upd' and row.Status == 'Completed':
        task_def = row.TaskDef
        if task_def.TaskCategory == 'START':
            update_next_task(row, old_row, logic_row)
            return True  # START task can always be completed
        dependencies = task_def.ToTaskTaskFlowList  # List of TaskFlow objects where this task is the ToTask
        for dependency in dependencies:
            from_task_def = dependency.FromTaskId
            to_task_def = dependency.ToTaskId
            from_task_instance = models.TaskInstance.query.filter_by(TaskId=from_task_def, StageId=row.StageId).first()
            if from_task_instance and from_task_instance.Status != 'Completed':
                logic_row.log(f"Cannot complete task {row.TaskInstanceId} because dependency task {from_task_instance.TaskInstanceId} is not completed.")
                return False
            
    #call_script_engine_pre(row, old_row, logic_row)
    #"All dependencies are completed."
    return True

def update_next_task(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    '''
    When a task is completed, update the next tasks in the workflow to be 'isPending' ready to start.
    '''
    if logic_row.ins_upd_dlt != 'upd' or row.Status != 'Completed':
        return # only proceed if the task was updated to 'Completed'
    task_id = row.TaskInstanceId
    task_def = row.TaskDef
    if not task_def:
        logic_row.log(f"No task definition found for TaskId {task.TaskId}")
        return
    logic_row.log(f'Task {task_id} completed. Checking for next tasks to set to isPending.')
    call_script_engine_post(row, old_row, logic_row) # call post script before updating next tasks
    for t in task_def.TaskFlowList:
        next_task_def = t.ToTaskId
        next_task_instance = models.TaskInstance.query.filter_by(TaskId=next_task_def, StageId=row.StageId).first()
        if next_task_instance:
            next_task_instance.Status = 'Pending'
            #session.add(next_task_instance)
            #session.commit()
            logic_row.log(f'Next task {next_task_instance.TaskInstanceId} set to isPending')
            logic_row.update(reason="Start task",row=next_task_instance)

            app_logger.info(f'Next task {next_task_instance.TaskInstanceId} set to isPending')
    
    return 

def call_script_engine_pre(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    task_def = row.TaskDef
    script = task_def.PreScriptJson or ''
    logic_row.log(f'PreScriptJson: {script}')
    if script != '':
        call_script_engine(row, old_row, logic_row, script)

def call_script_engine_post(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    task_def = row.TaskDef
    script = task_def.PostScriptJson or ''
    logic_row.log(f'PostScriptJson: {script}')
    if script != '':
        call_script_engine(row, old_row, logic_row, script)

def call_script_engine(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow, script: str):

    if logic_row.ins_upd_dlt == 'upd':  
        task_id = row.TaskInstanceId
        if row:
            # NOTE: may want to cascade the ResultData to subsequent tasks
            # depending on the workflow requirements
            task_def = row.TaskDef
            application_id = row.Stage.ProcessInstance.ApplicationId
            se = python_engine.PythonScriptEngine()
            context = {"data": row.to_dict(),"application_id": application_id, "task": row}
            external_context = {"get_application": get_application,"get_next_tasks":get_next_tasks, "models":models,"session":session,"db":db,"app_logger":app_logger,"Args":Args,"Config":Config,"datetime":datetime,"Decimal":Decimal,"logic_row": logic_row}
            r = se.execute(script=script, task=context, external_context=external_context)
            if r:
                app_logger.info(f'Script executed successfully for task_id {task_id}')
                row.ResultData = r.get('ResultData', None)
                print(f'Result: {row.ResultData}')

        else:
            app_logger.warning(f'No task found with task_id {task_id}') 

def declare_logic():
    pass

    Rule.constraint(validate=models.TaskInstance, calling=test_complete_task, error_msg="Cannot complete this task due to unmet dependencies not completed.")
    Rule.row_event(on_class=models.TaskInstance,calling=call_script_engine_pre)
    Rule.after_flush_row_event(on_class=models.TaskInstance, calling=call_script_engine_post)