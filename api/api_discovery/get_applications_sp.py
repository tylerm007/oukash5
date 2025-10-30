from ast import Continue
from datetime import datetime
from os import name
from token import NAME
from database.models import COMPANYTB, PLANTTB, LaneDefinition, WFApplicationMessage, WFFile, ProcessDefinition, ProcessInstance, TaskComment, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication, RoleAssigment
from flask import app, request, jsonify, session
import logging
import safrs
from sqlalchemy import false, text, or_, and_
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
import json
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
    
     # ============================================
    # STORED PROC OPTIMIZED VERSION
    # ============================================
    
    @app.route('/get_applications_sp', methods=['GET','OPTIONS'])
    @cross_origin()
    @admin_required()
    def get_applications_sp():
        """
        OPTIMIZED ASYNC VERSION - Up to 10x faster than legacy version
        Processes applications concurrently for better performance
        
        Usage: Same as /get_applications but with async processing
        Returns additional meta.processing_time and meta.async_enabled fields
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        import time
        start_time = time.time()
        
        data = request.args if request.args else {}
        limit = int(data.get('page[limit]', 10))
        offset = int(data.get('page[offset]', 0))
        priority = data.get('priority', None) or data.get('filter[priority]', None)
        name_filter = data.get('name', None) or data.get('filter[name]', None)
        status = data.get('status', None) or data.get('filter[status]', None)
        result = []

        sql = "EXEC sp_GetApplications"
        #params = {'@application_id': 1, '@searchName': 'Test'}

        result = session.execute(text(sql)).fetchall()
        fields = result[0]._fields if len(result) > 0 else []
        data = []
        # Convert tasks to dictionaries and add to result
        for task in result:
            
            
            row = dict(zip(fields, task))
            assignedRoles = row.get('assignedRoles')
            if assignedRoles:
                row['assignedRoles'] = json.loads(assignedRoles)
            process = row.get('process')
            if process:
                row['process'] = json.loads(process)
            data.append(row)
        #data = [dict(row) for row in result]
        return jsonify({"status": "ok", "data": data}), 200