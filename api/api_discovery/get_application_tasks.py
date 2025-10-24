from datetime import datetime
from unittest import result
from database.database_discovery.authentication_models import User
from database.models import LaneDefinition, WFApplicationMessage, WFFile,WFUSERROLE, ProcessDefinition, ProcessInstance, TaskComment, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication, RoleAssigment
from flask import app, request, jsonify, session
import logging
from httpx import get
import safrs
from sqlalchemy import false, text
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request

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

    def calc_days_between(start_date, end_date):
        if start_date and end_date:
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            return (end_date - start_date).days
        return 0
    

  

    @app.route('/get_application_tasks', methods=['GET','OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def get_application_tasks():
        """
        Retrieves the NCRC dashboard data
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:get_application_tasks?filter[application_id]=1&page[limit]=10&page[offset]=0' -Method GET).Content | ConvertFrom-Json

        $response = Invoke-WebRequest -Uri 'http://localhost:5656/get_application_tasks' -Method GET -Headers @{
            Authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDExNzM2NSwianRpIjoiNjJhY2M0NWItNjBmZS00OWM3LWE5OTYtNzgwOGQ4YTIwZTlmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzYwMTE3MzY1LCJleHAiOjE3NjAxMzA2ODV9.8ErMooyVGIz7vPh1IOPSnm6BasQk0XfQpZou1sZIVrI'
        }
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json
        
        To pretty-print the full JSON response in Python (like jq), you can use:
        
        print(json.dumps(response.json(), indent=2))
        # where 'response' is the result of requests.get(..., headers={"Authorization": "Bearer <token>"})
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.args if request.args else {}
        application_id = data.get('applicationId',None, type=int)
        user = get_jwt().get("sub", "unknown")
        app_logger.info(f"get_application_tasks called by user {user} with args: {data}")
        filter = data.get('filter', {})
        limit = int(data.get('page[limit]', 10))
        offset = int(data.get('page[offset]', 0))
        result = []
       
        args = request.args
        application_id = args.get('filter[applicationId]', None)
        plant_name = args.get('filter[plantName]', None)
        #application_id = args.get('applicationId', None)
        #plant_name = args.get('plantName', None)

        role_assignment = RoleAssigment.query.filter_by(Assignee=user).all() 
        assigned_roles = [role.WF_Role.UserRole for role in role_assignment]
        #user_roles = [role.WF_Role.UserRole for role in WFUSERROLE.query.filter_by(UserName=user).all()]
        
        # Convert list to comma-separated string for STRING_SPLIT function
        assigned_roles_str = ','.join(assigned_roles) if assigned_roles else 'NONE'
        
        app_logger.info(f"Calling stored procedure with: assignee={user}, assignee_role={assigned_roles_str}")
        
        try:
            tasks = session.execute(text('EXEC sp_GetTasksPerUser @username = :username, @applicationId = :applicationId, @plantName = :plantName'),{"username": user, "applicationId": application_id, "plantName": plant_name})
            tasks = tasks.fetchall()
            app_logger.info(f"Retrieved {len(tasks)} tasks from stored procedure")
        except Exception as e:
            app_logger.error(f"Error executing stored procedure: {e}")
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
        fields = tasks[0]._fields if len(tasks) > 0 else []
        
        # Convert tasks to dictionaries and add to result
        for task in tasks:
            task_dict = dict(zip(fields, task))
            # Apply additional filtering if needed
            task_role = task_dict.get("assigneeRole", "Unknown Role") 
            if can_user_run_task(user, task_role, task_dict.get("applicationId")):
                result.append(task_dict)
        
        return jsonify({"status": "ok", "data": result}), 200

    def can_user_run_task(user, task_role, application_id):
        if Args.instance.security_enabled == False:
            return True
        role_assignment = RoleAssigment.query.filter_by(ApplicationId=application_id).all() 
        assigned_roles = [role.WF_Role.UserRole for role in role_assignment]
        user_roles = [role.WF_Role.UserRole for role in WFUSERROLE.query.filter_by(UserName=user).all()]
        #if user in user_roles:
        #    return True
        if task_role in assigned_roles:
            return True
        return False
    
    @app.route('/get_application_tasks_orig', methods=['GET','OPTIONS'])
    @cross_origin()
    @admin_required()
    def get_application_tasks_orig():
        """
        Retrieves the NCRC dashboard data
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:get_application_tasks?filter[application_id]=1&page[limit]=10&page[offset]=0' -Method GET).Content | ConvertFrom-Json

        $response = Invoke-WebRequest -Uri 'http://localhost:5656/get_application_tasks' -Method GET -Headers @{
            Authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDA5NDA1NSwianRpIjoiNTA5Y2RjNzgtMzU2Mi00NGQ5LTgzZGQtNjZjZGRkZDkyMDYyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzYwMDk0MDU1LCJleHAiOjE3NjAxMDczNzV9.57vIy55dKdHwdX130fVmw0TmukcY4bgjKOGqUIhnIP8'
        }
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json
        
        To pretty-print the full JSON response in Python (like jq), you can use:
        
        print(json.dumps(response.json(), indent=2))
        # where 'response' is the result of requests.get(..., headers={"Authorization": "Bearer <token>"})
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.args if request.args else {}
        user = get_jwt().get("sub", "unknown")
        app_logger.info(f"get_application_tasks called by user {user} with args: {data}")
        filter = data.get('filter', {})
        limit = int(data.get('page[limit]', 10))
        offset = int(data.get('page[offset]', 0))
        result = []
        applications = WFApplication.query.order_by(WFApplication.CreatedDate.desc()).limit(limit).offset(offset).all() # to do add filter
        for app in applications:
            app_dict = app.to_dict()
            company_app = CompanyApplication.query.filter_by(ID=app_dict.get("ApplicationNumber")).first()
            if company_app == None:
                app_logger.warning(f"Legacy Application source not found for application id {app_dict.get('application_id')}")
                continue
            application_id = app_dict.get("ApplicationID", None)
            files = WFFile.query.filter_by(ApplicationID=application_id).all()
            app_messages = WFApplicationMessage.query.filter_by(ApplicationID=application_id).all()
            app_source = company_app.to_dict() if company_app else {}
            # Calculate days between CreateDate and ModifiedDate
            created_date = app_dict.get("CreatedDate")
            modified_date = app_dict.get("ModifiedDate")
            days_between = calc_days_between(created_date, modified_date)
            #process_id = app_dict.get("ProcessId")
            role_assignment = RoleAssigment.query.filter_by(ApplicationId=application_id).all() 
            assigned_roles = [role.WF_Role.UserRole for role in role_assignment]
            status = get_app_status(app_dict.get("Status"))
            app_row = {
                "id": application_id,
                "company": app_source.get("CompanyName"),
                "plant": app_source.get("PlantName"),
                "plantHistory": {},
                "applicationId": application_id,
                "region": app_source.get("Region"),
                "priority": app_dict.get("Priority", "Normal"),
                "status": status,
                "assignedRC": app_source.get("AssignedTo"),
                "daysInStage": days_between,
                "overdue": days_between > 10,
                "lastUpdate": modified_date,
                "nextAction": "Follow up on contract",
                "documents": len(files) if files else 0,
                "notes": len(app_messages) if app_messages else 0,
                "aiSuggestions": {},
                "assignedRC": app_source.get("AssignedTo","Unassigned"),
                "assignedRoles": [{ role.WF_Role.UserRole: role.Assignee} for role in role_assignment]
            }
            
          
            if application_id:
                process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
                if process_instance is None:
                    app_logger.warning(f"Process instance not found for application id {application_id}")
                    return jsonify({"status": "error", "message": f"Workflow Process instance not found for application id {application_id}"}), 404
                stages =  [stage.to_dict() for stage in StageInstance.query.filter_by(ProcessInstanceId=process_instance.InstanceId).order_by(StageInstance.StageInstanceId).all()]
                user_roles = [role.WF_Role.UserRole for role in RoleAssigment.query.filter_by(ApplicationId=application_id, Assignee=user).all()]
                if stages is None:
                    app_logger.warning(f"Stages not found for application id {application_id}")
                    return jsonify({"status": "error", "message": f"Workflow Stages not found for application id {application_id}"}), 404
                app_row["stages"] = {}
                for stage in stages:
                    tasks = []
                    task_cnt = 0
                    completed_cnt = 0
                    # Filter by role using the user to get the roles
                    
                    # Get tasks for the stage
                    task_instances = TaskInstance.query.filter_by(StageId=stage['StageInstanceId']).order_by(TaskInstance.TaskInstanceId).all()
                    for task in task_instances:
                        if task.TaskDef.AutoComplete == True or task.TaskDef.TaskType in ['START','END',"LANESTART",'LANEEND', 'GATEWAY']:
                            continue
                        
                        task_cnt += 1 #if task.Status == 'PENDING' else 0
                        completed_cnt += 1 if task.Status == 'COMPLETED' else 0
                        created_date = task.StartedDate
                        modified_date = datetime.now() if task.Status != 'COMPLETED' else task.CompletedDate
                        days_between = calc_days_between(created_date, modified_date)
                        task_role = task.TaskDef.AssigneeRole if task and task.TaskDef else "Unknown Role" 
                        if task_role not in assigned_roles:
                            continue
                        if task.Status != 'PENDING':
                            continue
                        tasks.append(
                            {
                                "name": task.TaskDef.TaskName if task and task.TaskDef else "Unknown Task Name",
                                "status": task.Status,
                                "taskType": task.TaskDef.TaskType if task and task.TaskDef else "Unknown Task Type",
                                "taskCategory": task.TaskDef.TaskCategory if task and task.TaskDef else "Unknown Task Category",
                                "assignee": task.AssignedTo,
                                "daysActive": days_between,
                                "description": task.TaskDef.Description if task and task.TaskDef else " ",
                                "required": task.TaskDef.IsRequired if task and task.TaskDef else False,
                                "TaskInstanceId": task.TaskInstanceId,
                                "PreScript": getPreScript(task),
                                #"PostScript": task.TaskDef.PostScriptJson if task and task.TaskDef else {},
                                "taskRoles": [
                                    { "taskRole": task_role},
                                ],
                            }
                        )
                    lane = LaneDefinition.query.filter_by(LaneId=stage['LaneId']).first()
                    if lane and len(tasks) > 0:
                        lane_name = lane.to_dict()["LaneName"]
                        app_row["stages"].update({
                            lane_name: {
                                "status": stage["Status"], 
                                "progress": int(completed_cnt / task_cnt * 100) if task_cnt > 0 and  completed_cnt > 0 else 0,
                                "tasks": tasks
                            }
                        })
            
            app_row["application_messages"] =[]
            #task_messages = TaskComment.query.filter_by(ApplicationId=application_id).order_by(TaskComment.CreatedOn.desc()).limit(5).all()
            for am in app_messages:
                msg = am.to_dict()
                app_row["application_messages"].append({
                    "id": msg.get("MessageID"),
                    "fromUser": msg.get("FromUser"), 
                    "toUser": msg.get("ToUser"),
                    "priority": msg.get("Priority"),
                    "text": msg.get("MessageText"),
                    "sentDate": msg.get("SentDate"),
                    "messageType": msg.get("MessageType"),
                    #"isSystemMessage": True if msg.get("MessageType") == "system" else False,
                })
            files = [] #WFFile.query.filter(WFFile.FilePath != None).all() #TODO ApplicationId=application_id 
            app_row['files'] = []
            for file in files:
                app_row['files'].append({
                    "id": file.FileID if hasattr(file, 'FileID') else None,
                    "fileName": file.FileName if hasattr(file, 'FileName') else "Unknown File",
                    "filePath": file.FilePath if hasattr(file, 'FilePath') else "/path/to/file",
                    "fileType": file.FileType if hasattr(file, 'FileType') else "PDF",
                    "fileSize": file.FileSize if hasattr(file, 'FileSize') else " "
                })
            result.append(app_row)
        return jsonify({"status": "ok", "data": result}), 200
    
    def getPreScript(task: TaskInstance):
        script = task.TaskDef.PreScriptJson if task and task.TaskDef else {}
        from jinja2 import Template
        if script and isinstance(script, str) and '{{' in script:
            template = Template(script)
            title = task.TaskDef.TaskName if task and task.TaskDef else "Unknown Task Name"
            description = task.TaskDef.Description if task and task.TaskDef else " "
            application_id = task.Stage.ProcessInstance.ApplicationId if task and task.Stage and task.Stage.ProcessInstance else None
            task_id = task.TaskInstanceId if task else None
            script = template.render(Title=title, Description=description, ApplicationID=application_id, TaskInstanceId=task_id)

        return script
    def getPostScript(task: TaskInstance):
        return task.TaskDef.PostScriptJson if task and task.TaskDef else {}
    
    def get_app_status(status_code: str):
        status_map = {
            "NEW": "New",
            "INP": "In Progress",
            "HLD": "On Hold",
            "WTH": "Withdrawn",
            "COMPL": "Completed",
            "REJ": "Rejected"
        }
        return status_map.get(status_code, "Unknown Status")