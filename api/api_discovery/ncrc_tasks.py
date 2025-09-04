from datetime import datetime
import re
from tracemalloc import start
from database.models import LaneDefinition, ProcessDefinition, ProcessInstance, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication
from flask import app, request, jsonify, session
import logging
import safrs
from sqlalchemy import false

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass

    @app.route('/get_ncrc_applications', methods=['GET','OPTIONS'])
    def get_ncrc_applications():
        """
        Retrieves the NCRC dashboard data
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:5656/get_ncrc_applications?filter[application_id]=1&page[limit]=10&page[offset]=0' -Method GET).Content | ConvertFrom-Json

        $response = Invoke-WebRequest -Uri 'http://localhost:5656/get_ncrc_applications' -Method GET
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.args if request.args else {}
        filter = data.get('filter', {})
        limit = data.get('page[limit]', 10)
        offset = data.get('page[offset]', 0)
        result = []
        applications = WFApplication.query.all() #limit(limit).offset(offset).all() # to do add filter
        for app in applications:
            app_dict = app.to_dict()
            company_app = CompanyApplication.query.filter_by(ID=app_dict.get("ApplicationNumber")).first()
            if company_app == None:
                app_logger.warning(f"Legacy Application source not found for application id {app_dict.get('application_id')}")
                continue
            application_id = app_dict.get("ApplicationID", None)
            app_source = company_app.to_dict() if company_app else {}
            app_row = {
                "id": application_id,
                "company": app_source.get("CompanyName"),
                "plant": app_source.get("PlantName"),
                "region": "NY Metro",
                "priority": "high",
                "status": "contract_sent",
                "assignedRC": "R. Gorelik",
                "daysInStage": 3,
                "overdue": false,
                "lastUpdate": "2025-08-23",
                "nextAction": "Follow up on contract",
                "documents": 12,
                "notes": 3
            }
            
          
            if application_id:
                process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
                if process_instance is None:
                    app_logger.warning(f"Process instance not found for application id {application_id}")
                    return jsonify({"status": "error", "message": f"Workflow Process instance not found for application id {application_id}"}), 404
                stages =  [stage.to_dict() for stage in StageInstance.query.filter_by(ProcessInstanceId=process_instance.InstanceId).all()]
                app_row["stages"] = {}
                tasks = []
                for stage in stages:
                    task_instances = TaskInstance.query.filter_by(StageId=stage['StageInstanceId']).all()
                    for task in task_instances:
                        tasks.append(
                            {
                                "name": task.TaskDef.TaskName if task and task.TaskDef else "Unknown Task",
                                "status": task.Status,
                                "assignee": task.AssignedTo,
                                "daysActive": 0,
                                "required": task.TaskDef.IsRequired if task and task.TaskDef else False,
                                "TaskId": task.TaskId
                            }
                        )
                    lane = LaneDefinition.query.filter_by(LaneId=stage['LaneId']).first()
                    if lane:
                        lane_name = lane.to_dict()["LaneName"]
                        app_row["stages"].update({
                            lane_name: {
                                "status": stage["Status"],
                                "progress": 100,
                                "tasks": tasks
                            }
                        })
            app_row["aiSuggestions"] = {}
            app_row["plantHistory"] = {}
            app_row["relatedTasks"] = {}
            app_row["task_messages"] = {}
            result.append(app_row)
        return jsonify({"status": "ok", "data": result}), 200

    @app.route('/get_ncrc_tasks', methods=['GET','OPTIONS'])
    def get_ncrc_dashboard_tasks():
        """
        Retrieves the NCRC dashboard data
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:5656/get_ncrc_tasks?application_id=1' -Method GET).Content | ConvertFrom-Json

        $response = Invoke-WebRequest -Uri 'http://localhost:5656/get_ncrc_tasks?application_id=1' -Method GET
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
