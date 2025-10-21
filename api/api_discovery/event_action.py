from ast import Is
from datetime import datetime
from database import models
from database.models import INVOICEFEE, EventAction, TaskDefinition, ProcessInstance, WFApplication, WorkflowHistory, StageInstance, TaskInstance, LaneDefinition, TaskFlow , ProcessMessage, WFApplicationMessage
from flask import request, jsonify, session
import logging
from logic.logic_discovery.workflow_engine import call_script_engine_post, call_task_script_engine
from oracledb import EVENT_AQ
import safrs
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from datetime import timedelta


app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
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
    
    # ==================================================
    #        WORKFLOW EventAction ENDPOINTS (Flask)
    # ==================================================
   
    @app.route('/create_event', methods=['POST','OPTIONS'])
    @admin_required()
    @jwt_required()
    def create_event():

        if request.method == 'OPTIONS':
            return jsonify({"status": "OK"}), 200
        
        data = request.get_json()
        task_instance_id = data.get('TaskInstanceId')
        event_key = data.get('EventKey')  
        _create_event(task_instance_id, event_key)
        return jsonify({"status": "Event created"}), 200


    @app.route('/resolve_event', methods=['POST','OPTIONS'])
    @admin_required()
    @jwt_required()
    def resolve_event():
        
        if request.method == 'OPTIONS':
            return jsonify({"status": "OK"}), 200
        
        data = request.get_json()
        #task_instance_id = data.get('TaskInstanceId')
        event_key = data.get('EventKey')  
        _resolve_event(event_key)
        return jsonify({"status": "Event resolved"}), 200
    

def _create_event(task_instance_id: int, event_key: str) -> EventAction:
    """Create an event action for a task instance."""
    event_action = EventAction(
        TaskInstanceId=task_instance_id,
        EventKey=event_key,
        EventStatus='PENDING',
        EventMessage='Event created via API',
        StartDate=datetime.utcnow(),
        DueDate=datetime.utcnow() + timedelta(days=1),
        IsResolved=False
    )
    session.add(event_action)
    session.commit()
    app_logger.info(f"Event created: TaskInstanceId={task_instance_id}, EventKey={event_key}")
    return event_action

def _resolve_event(event_key: str):
    """Resolve an event action for a task instance."""
    event_action = session.query(EventAction).filter_by(
        EventKey=event_key,
        EventStatus='PENDING',
        IsResolved=False
    ).first()
    
    if event_action:
        event_action.EventStatus = 'RESOLVED'
        event_action.ResolvedDate = datetime.utcnow()
        event_action.IsResolved = True
        session.commit()
        app_logger.info(f"Event resolved: EventKey={event_key}")
    else:
        app_logger.warning(f"No matching EventAction found to resolve for EventKey={event_key}")


def _create_invoice_fee(company_id: int, fee_amount: float) -> INVOICEFEE:
    """Create an invoice fee record."""
    #TODO Hardcode NULL Status and existing Invoice - we cannot insert into table
    invoice_fee = session.query(INVOICEFEE).filter(INVOICEFEE.COMPANY_ID == 12034, INVOICEFEE.STATUS != 'Paid').first()
    if not invoice_fee:
        invoice_fee = INVOICEFEE(
            INVOICE_ID=None, # NOT AUTONUM
            COMPANY_ID=company_id,
            TOTAL_AMOUNT=fee_amount,
            INVOICE_TYPE = 'Visit',
            TYPE = 'KIM',
            STATUS = '',
            INVOICE_DATE=datetime.utcnow()
        )
        #session.add(invoice_fee)
        try:
           # session.commit()
           pass
        except Exception as e:
            session.rollback()  
            app_logger.error(f"Error creating invoice fee: {e}")
    app_logger.info(f"Invoice fee created: CompanyId={company_id}, FeeAmount={fee_amount}")
    return invoice_fee