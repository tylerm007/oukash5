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
    task_def = row.TaskDef
    dependencies = task_def.FromTaskTaskFlowList  # List of TaskFlow objects where this task is the ToTask
    for dependency in dependencies:
        from_task_def = dependency.FromTaskDef
        from_task_instance = models.TaskInstance.query.filter_by(TaskId=from_task_def.TaskId, StageId=row.StageId).first()
        if from_task_instance and from_task_instance.Status != 'completed':
            return False, f"Cannot complete task {row.TaskInstanceId}. Dependency task {from_task_instance.TaskInstanceId} is not completed."
    return True, "All dependencies are completed."

def update_next_task(task_id: int):
    '''
    When a task is completed, update the next tasks in the workflow to be 'isPending' ready to start.
    '''
    task = models.TaskInstance.query.filter_by(TaskInstanceId=task_id).first()
    if not task:
        return None, jsonify({"success": False, "message": f"No task found with TaskInstanceId {task_id}"}), 404
    task_def = TaskDefinition.query.filter_by(TaskId=task.TaskId).first()
    if not task_def:
        return None, jsonify({"success": False, "message": f"No task definition found for TaskId {task.TaskId}"}), 404
    next_task_list = []
    for t in task_def.ToTaskTaskFlowList:
        next_task_def = t.ToTaskDef
        next_task_instance = models.TaskInstance.query.filter_by(TaskId=next_task_def.TaskId, StageId=task.StageId).first()
        if next_task_instance:
            next_task_list.append(next_task_instance.to_dict().TaskInstanceId)

    return next_task_list

def call_script_engine_pre(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    task_def = row.TaskDef
    script = task_def.PreScriptJson or ''
    logic_row.log(f'PreScriptJson: {script}')
    call_script_engine(row, old_row, logic_row, script)

def call_script_engine_post(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):
    task_def = row.TaskDef
    script = task_def.PostScriptJson or ''
    logic_row.log(f'PostScriptJson: {script}')
    call_script_engine(row, old_row, logic_row, script)

def call_script_engine(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow, script: str):

    if logic_row.ins_upd_dlt == 'upd':  
        task_id = row.TaskInstanceId
        if row:
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

    # add logic here if needed
    Rule.row_event(on_class=models.TaskInstance,calling=call_script_engine_pre)
    Rule.after_flush_row_event(on_class=models.TaskInstance, calling=call_script_engine_post)