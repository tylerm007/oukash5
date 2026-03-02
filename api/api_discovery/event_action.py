from datetime import datetime
from database.models import EventAction , INVOICEFEE
from flask import request, jsonify, session, has_request_context
import logging
import flask
#from logic.logic_discovery.workflow_engine import call_script_engine_post, call_task_script_engine
import safrs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required
from datetime import timedelta, datetime, timezone
from logic_bank.exec_row_logic.logic_row import LogicRow
from security.system.authorization import Security


app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None
from functools import wraps
from flask import request, jsonify



def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass

    # ==================================================
    #        WORKFLOW EventAction ENDPOINTS (Flask)
    # ==================================================
   
    @app.route('/create_event', methods=['POST','OPTIONS'])
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
    @jwt_required()
    def resolve_event():
        
        if request.method == 'OPTIONS':
            return jsonify({"status": "OK"}), 200
        
        access_token = request.headers.get('Authorization')
        user = Security.current_user().Username
        data = request.get_json()
        #task_instance_id = data.get('TaskInstanceId')
        event_key = data.get('EventKey')  
        _resolve_event(event_key, user, access_token)
        return jsonify({"status": "Event resolved"}), 200
    
    @app.route('/resolve_paid_invoices', methods=['GET','OPTIONS'])
    @jwt_required()
    def resolve_invoices():
        
        if request.method == 'OPTIONS':
            return jsonify({"status": "OK"}), 200
        access_token = request.headers.get('Authorization') 
        user = Security.current_user().Username
        resolve_paid_invoices(access_token=access_token, user=user)
        return jsonify({"status": 'ok', "message": "All EventActions resolved"}), 200
    
def resolve_paid_invoices(access_token: str = None, user: str = 'system', app: flask = None):
    """Resolve EventActions for paid invoices."""
    from flask import current_app, has_request_context
    
    app_logger.info(f"🔍 resolve_paid_invoices called with app={app is not None}")
    
    # Get the Flask app instance
    if not app:
        try:
            app = current_app._get_current_object()
            app_logger.info("✅ Got Flask app from current_app")
        except RuntimeError:
            # If no current app, we need to get it from somewhere
            app_logger.error("❌ No Flask app context available - background task may fail")
            app_logger.error("   This indicates the background task is not running with proper Flask context")
            app_logger.error("   Check that the background scheduler is initialized with the Flask app")
            return
    
    # Run everything within Flask application context
    with app.app_context():
        try:
            from api.api_discovery.event_action import _resolve_event
            import requests
            
            # Try to get token from request context if available (when called from endpoint)
            if not access_token:
                try:
                    # Only try to access request if we're in a request context
                    if has_request_context():
                        access_token = request.headers.get('Authorization')
                        user = Security.current_user().Username
                except RuntimeError:
                    # Working outside of request context - this is expected for background tasks
                    pass
            
            # If still no token, get system token for background processing
            if not access_token:
                app_logger.info("Getting system token for background task")
                try:
                    payload = {"username": "admin", "password": "p"}
                    # Fix the URL (was missing one colon)
                    url = f'{Args.instance.http_scheme}://{Args.instance.swagger_host}:{Args.instance.swagger_port}/api/auth/login'
                    r = requests.post(url, json=payload, verify=False)
                    if r.status_code == 200:
                        access_token = r.json().get("access_token")
                        user = 'system'
                        app_logger.info("✅ System token obtained for background task")
                    else:
                        app_logger.warning(f"Failed to get system token: {r.status_code}")
                except Exception as auth_error:
                    app_logger.warning(f"Could not get system token: {auth_error}")
                    # Continue without token for demo purposes
                    access_token = None
                    user = 'system'
            
            if not user:
                user = 'system'
            
            app_logger.info(f"Processing pending EventActions as user: {user}")
            
            # Get all pending event actions (now within app context)
            event_actions = session.query(EventAction).filter_by(
                EventStatus='PENDING', 
                IsResolved=False
            ).all()
            
            app_logger.info(f"Found {len(event_actions)} pending EventActions to resolve")
            
            resolved_count = 0
            for event_action in event_actions:
                try:
                    _resolve_event(event_action.EventKey, user, access_token)
                    resolved_count += 1
                except Exception as resolve_error:
                    app_logger.error(f"Error resolving event {event_action.EventKey}: {resolve_error}")
                    continue
            
            app_logger.info(f"✅ Resolved {resolved_count}/{len(event_actions)} EventActions")
            
        except Exception as e:
            app_logger.error(f"Error resolving paid invoices: {e}")
            session.rollback()
    
def _create_event(task_instance_id: int, event_key: str, logic_row: LogicRow = None) -> EventAction:
    """Create an event action for a task instance."""
    event_action = session.query(EventAction).filter_by(TaskInstanceId=task_instance_id, EventKey=event_key).first()
    if event_action:
        app_logger.info(f"Event already exists: TaskInstanceId={task_instance_id}, EventKey={event_key}")
        return event_action
    event_action = EventAction(
        TaskInstanceId=task_instance_id,
        EventKey=event_key,
        EventStatus='PENDING',
        EventMessage='Event created via API',
        StartDate=datetime.now(),
        DueDate=datetime.now() + timedelta(days=1),
        IsResolved=False
    )
    session.add(event_action)
    if logic_row:
        logic_row.update(f"EventAction created: TaskInstanceId={task_instance_id}, EventKey={event_key}", event_action)
    else:
        session.commit()
    app_logger.info(f"Event created: TaskInstanceId={task_instance_id}, EventKey={event_key}")
    return event_action

def _resolve_event(event_key: str, user: str, logic_row: LogicRow = None, access_token: str = None):
    """Resolve an event action for a task instance."""
    event_action = session.query(EventAction).filter_by(
        EventKey=event_key,
        EventStatus='PENDING',
        IsResolved=False
    ).first()
    
    if event_action:
        event_action.EventStatus = 'RESOLVED'
        event_action.ResolvedDate = datetime.now()
        event_action.IsResolved = True
        try:
            if logic_row:
                logic_row.update(f"EventAction resolved: EventKey={event_key}", event_action)
            else:
                session.commit()
                session.flush()
            app_logger.info(f"Event resolved: EventKey={event_key}")
            from api.api_discovery.complete_task import _complete_task
            _complete_task(event_action.TaskInstanceId, result=None, completed_by=user, completion_notes='EventAction resolved', access_token=access_token, depth=0)
        except Exception as e:
            #session.rollback()
            app_logger.error(f"Error committing event resolution: {e}")
    else:
        app_logger.warning(f"No matching EventAction found to resolve for EventKey={event_key}")
    return
    


def _create_invoice_fee(company_id: int, fee_amount: float, logic_row: LogicRow = None) -> any:
    """Create an invoice fee record."""
    #TODO Hardcode NULL Status and existing Invoice - we cannot insert into table
    invoice_fee = session.query(INVOICEFEE).filter(INVOICEFEE.COMPANY_ID == company_id, INVOICEFEE.STATUS != 'Paid').first()
    if not invoice_fee:
        invoice_fee = INVOICEFEE(
            INVOICE_ID=None, # NOT AUTONUM
            COMPANY_ID=company_id,
            TOTAL_AMOUNT=fee_amount,
            INVOICE_TYPE = 'Visit',
            TYPE = 'KIM',
            STATUS = '',
            INVOICE_DATE=datetime.now()
        )
        session.add(invoice_fee)
        try:
            if logic_row:
                logic_row.update(f"InvoiceFee created: CompanyId={company_id}, FeeAmount={fee_amount}", invoice_fee)
            else:   
                session.commit()
                session.flush()
        except Exception as e:
            #session.rollback()  
            app_logger.error(f"Error creating invoice fee: {e}")
    app_logger.info(f"Invoice fee created: CompanyId={company_id}, FeeAmount={fee_amount}")
    return invoice_fee