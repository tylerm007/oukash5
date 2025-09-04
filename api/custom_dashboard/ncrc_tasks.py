from asyncio import Task
from datetime import datetime
import re
from tracemalloc import start
from database.models import LaneDefinition, ProcessDefinition, ProcessInstance, TaskInstance
from flask import app, request, jsonify, session
import logging
import pyodbc
import uuid
import safrs

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass


    @app.route('/getNCRCDashboardTasks', methods=['GET','OPTIONS'])
    def get_ncrc_dashboard_tasks():
        """
        Retrieves the NCRC dashboard data
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:5656/getNCRCDashboardTasks?application_id=1' -Method GET).Content | ConvertFrom-Json

        $response = Invoke-WebRequest -Uri 'http://localhost:5656/getNCRCDashboardTasks?application_id=1' -Method GET
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        data = request.args if request.args else {}
        application_id = data.get('application_id', None)
        if application_id is None:
            return jsonify({"status": "error", "message": "application_id is required"}), 400
        
        app_logger.info('Retrieving NCRC dashboard data')
        # Implement your logic to retrieve and return the NCRC dashboard data:
        from database.models import WFApplication, ProcessInstance, TaskInstance
        app_obj = WFApplication.query.filter_by(ApplicationID=application_id).first()
        if not app_obj:
            return jsonify({"status": "error", "message": "Application not found"}), 404    
        
        process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
        if process_instance is None:
            return jsonify({"status": "error", "message": "Process instance not found or workflow not started"}), 404
        result = {}
        result['process_instance'] = process_instance.to_dict() if process_instance else {}
        stage_list = process_instance.StageInstanceList if process_instance else []
        result['stages'] = {}
        #[stage.to_dict() if stage else {} for stage in stage_list]
        for stage in stage_list:
            result['stages'][stage.Lane.LaneName] = {
                "stage_info": stage.to_dict() if stage else {},
                "tasks": []
            }
            tasks = stage.TaskInstanceList if stage else []
            for task in tasks:
                result['stages'][stage.Lane.LaneName]['tasks'].append(task.to_dict() if task else {})
        return jsonify({"status": "ok", "data": result}), 200
