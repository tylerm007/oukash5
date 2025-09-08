from datetime import datetime
from math import log
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

def test(row: models.TaskInstance, old_row: models.TaskInstance, logic_row: LogicRow):

    if logic_row.ins_upd_dlt == 'upd':  
        task_id = row.TaskInstanceId
        if row:
            task_def = row.TaskDef
            application_id = row.Stage.ProcessInstance.ApplicationId
            se = python_engine.PythonScriptEngine()
            script = task_def.PreScriptJson or ''
            context = {"data": row.to_dict(),"application_id": application_id}
            external_context = {"get_application": get_application}
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
    Rule.row_event(on_class=models.TaskInstance,calling=test)