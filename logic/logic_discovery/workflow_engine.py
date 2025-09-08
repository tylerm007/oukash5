from datetime import datetime
from math import log
from operator import call
from database.models import TaskInstance
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
            external_context = {"get_application": get_application,"models":models,"session":session,"db":db,"app_logger":app_logger,"Args":Args,"Config":Config,"datetime":datetime,"Decimal":Decimal,"logic_row": logic_row}
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