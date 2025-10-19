from datetime import datetime
from database.models import LaneDefinition, WFApplicationMessage, WFFile, ProcessDefinition, ProcessInstance, TaskComment, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication, RoleAssigment
from flask import app, request, jsonify, session
import logging
import safrs
from sqlalchemy import false
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
    
    @app.route('/get_applications', methods=['GET','OPTIONS'])
    @cross_origin()
    @admin_required()
    def get_applications():
        """
        Retrieves the NCRC dashboard data
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:5656_applications?filter[application_id]=1&page[limit]=10&page[offset]=0' -Method GET).Content | ConvertFrom-Json

        $response =Invoke-WebRequest -Uri 'http://localhost:5656/get_applications' -Method GET -Headers @{
            Authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDA5NDA1NSwianRpIjoiNTA5Y2RjNzgtMzU2Mi00NGQ5LTgzZGQtNjZjZGRkZDkyMDYyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzYwMDk0MDU1LCJleHAiOjE3NjAxMDczNzV9.57vIy55dKdHwdX130fVmw0TmukcY4bgjKOGqUIhnIP8'
        }
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json

        To pretty-print the full JSON response in Python (like jq), you can use:
        
        print(json.dumps(response.json(), indent=2))
        # where 'response' is the result of requests.get(...)
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.args if request.args else {}
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
            status = get_app_status(app_dict.get("Status"))
            days_between = calc_days_between(created_date, modified_date)  if status == "INP" else 0
            #process_id = app_dict.get("ProcessId")
            assigned_roles = RoleAssigment.query.filter_by(ApplicationId=application_id).all() 
            
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
                "overdue": days_between > 1 if status == "INP" else False,
                "lastUpdate": modified_date,
                "nextAction": "Follow up on contract",
                "documents": len(files) if files else 0,
                "notes": len(app_messages) if app_messages else 0,
                "aiSuggestions": {},
                "assignedRC": app_source.get("AssignedTo","Unassigned"),
                "assignedRoles": [{ role.WF_Role.UserRole: role.Assignee} for role in assigned_roles]
            }
            
          
            if application_id:
                process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
                if process_instance is None:
                    app_logger.warning(f"Process instance not found for application id {application_id}")
                    return jsonify({"status": "error", "message": f"Workflow Process instance not found for application id {application_id}"}), 404
                stages =  [stage.to_dict() for stage in StageInstance.query.filter_by(ProcessInstanceId=process_instance.InstanceId).order_by(StageInstance.StageInstanceId).all()]
                if stages is None:
                    app_logger.warning(f"Stages not found for application id {application_id}")
                    return jsonify({"status": "error", "message": f"Workflow Stages not found for application id {application_id}"}), 404
                app_row["stages"] = {}
                for stage in stages:
                    tasks = []
                    task_cnt = 0
                    completed_cnt = 0
                    task_instances = TaskInstance.query.filter_by(StageId=stage['StageInstanceId']).order_by(TaskInstance.TaskInstanceId).all()
                    for task in task_instances:
                        if task.TaskDef.AutoComplete == True or task.TaskDef.TaskType in ['START','END',"LANESTART",'LANEEND']:
                            continue
                        task_cnt += 1 #if task.Status == 'PENDING' else 0
                        completed_cnt += 1 if task.Status == 'COMPLETED' else 0
                        created_date = task.StartedDate
                        modified_date = datetime.now() if task.Status != 'COMPLETED' else task.CompletedDate
                        days_between = calc_days_between(created_date, modified_date)
                        tasks.append(
                            {
                                "name": task.TaskDef.TaskName if task and task.TaskDef else "Unknown Task Name",
                                "status": task.Status,
                                "taskType": task.TaskDef.TaskType if task and task.TaskDef else "Unknown Task Type",
                                "taskCategory": task.TaskDef.TaskCategory if task and task.TaskDef else "Unknown Task Category",
                                "assignee": task.AssignedTo,
                                "daysActive": days_between,
                                "overdue": days_between > 1 and task.Status != 'COMPLETED',
                                "createdDate": task.StartedDate,
                                "description": task.TaskDef.Description if task and task.TaskDef else " ",
                                "required": task.TaskDef.IsRequired if task and task.TaskDef else False,
                                "TaskInstanceId": task.TaskInstanceId,
                                "PreScript": getPreScript(task),
                                "CompletedDate": task.CompletedDate,
                                "Result": task.Result,
                                "ResultData": task.ResultData,
                                "ErrorMessage": task.ErrorMessage,
                                #"PostScript": task.TaskDef.PostScriptJson if task and task.TaskDef else {},
                                "taskRoles": [
                                    { "taskRole": task.TaskDef.AssigneeRole if task and task.TaskDef else "Unknown Role" },
                                ],
                            }
                        )
                    lane = LaneDefinition.query.filter_by(LaneId=stage['LaneId']).first()
                    if lane: # and len(tasks) > 0:
                        lane_name = lane.to_dict()["LaneName"]
                        app_row["stages"].update({
                            lane_name: {
                                "status": stage["Status"], 
                                "description": lane.to_dict()["LaneDescription"],
                                "progress": int(completed_cnt / task_cnt * 100) if task_cnt > 0 and  completed_cnt > 0 else 0,
                                "tasks": tasks
                            }
                        })
            app_row["aiSuggestions"] = {}
            app_row["plantHistory"] = {}
            app_row["relatedTasks"] = {}
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
            files = WFFile.query.filter(WFFile.FilePath != None).all() #TODO ApplicationId=application_id 
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
        default_script = ''' 
            {
                "Title": "{{ Title }}",
                "Description": "{{ Description }}",
                "ApplicationID": "{{ ApplicationID }}",
                "TaskInstanceId": "{{ TaskInstanceId }}"
            }
        '''
        script = task.TaskDef.PreScriptJson if task and task.TaskDef and task.TaskDef.PreScriptJson else {}
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