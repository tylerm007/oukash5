#from ast import Is
from datetime import datetime
from os import access
import re
from database import models
from database.database_discovery.authentication_models import User
from database.models import INVOICEFEE, EventAction, TaskDefinition, ProcessInstance, WFApplication, WorkflowHistory, StageInstance, TaskInstance, LaneDefinition, TaskFlow , ProcessMessage, WFApplicationMessage
from flask import request, jsonify, session, has_request_context
import logging
import flask
from logic.logic_discovery.workflow_engine import call_script_engine_post, call_task_script_engine
from oracledb import EVENT_AQ
import safrs
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from datetime import timedelta

from security.system.authorization import Security


app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None
from functools import wraps
from flask import request, jsonify
import requests

COGNITO_REGION = 'us-east-1'
COGNITO_POOL_ID = Config.COGNITO_USER_POOL_ID #'us-east-1_xxxxxx'
JWKS_URL = f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}/.well-known/jwks.json'

# Cache JWKS
jwks = requests.get(JWKS_URL).json()


def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass
    #Working with AWS Cognito Tokens
    #Since you're using Cognito, you'll also need to configure Flask-JWT-Extended to work with Cognito's tokens:
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
    '''
    def require_cognito_jwt(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing token'}), 401
            
            token = auth_header.split(' ')[1]
            
            try:
                claims = jwt.decode(
                    token,
                    jwks,
                    algorithms=['RS256'],
                    audience=Config.COGNITO_CLIENT_ID,
                    issuer=f'https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}'
                )
                # Attach claims to request context
                request.cognito_claims = claims
                return f(*args, **kwargs)
            except JWTError as e:
                return jsonify({'error': f'Invalid token - {str(e)}'}), 401
        
        return decorated_function
    ''' 
    @app.route('/api/protected')
    #@require_cognito_jwt
    def protected():
        claims = request.cognito_claims
        return {'user_name': claims['app_username']}

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
        
        access_token = request.headers.get('Authorization')
        user = Security.current_user().id
        data = request.get_json()
        #task_instance_id = data.get('TaskInstanceId')
        event_key = data.get('EventKey')  
        _resolve_event(event_key, user, access_token)
        return jsonify({"status": "Event resolved"}), 200
    
    @app.route('/resolve_paid_invoices', methods=['GET','OPTIONS'])
    @admin_required()
    @jwt_required()
    def resolve_invoices():
        
        if request.method == 'OPTIONS':
            return jsonify({"status": "OK"}), 200
        access_token = request.headers.get('Authorization') 
        user = Security.current_user().id
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
                        user = Security.current_user().id
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
                    r = requests.post(url, json=payload)
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

def _resolve_event(event_key: str, user: str, access_token: str = None):
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
        try:
            session.commit()
            app_logger.info(f"Event resolved: EventKey={event_key}")
            from api.api_discovery.complete_task import _complete_task
            _complete_task(event_action.TaskInstanceId, result=None, completed_by=user, completion_notes='EventAction resolved', access_token=access_token, depth=0)
        except Exception as e:
            session.rollback()
            app_logger.error(f"Error committing event resolution: {e}")
    else:
        app_logger.warning(f"No matching EventAction found to resolve for EventKey={event_key}")
    return
    


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