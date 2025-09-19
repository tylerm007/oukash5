from datetime import datetime
from database.models import LaneDefinition, WFApplicationMessage, WFFile, ProcessDefinition, ProcessInstance, TaskComment, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication, RoleAssigment
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
    def calc_days_between(start_date, end_date):
        if start_date and end_date:
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            return (end_date - start_date).days
        return 0
    @app.route('/get_applications', methods=['GET','OPTIONS'])
    def get_applications():
        """
        Retrieves the NCRC dashboard data
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:5656_applications?filter[application_id]=1&page[limit]=10&page[offset]=0' -Method GET).Content | ConvertFrom-Json

        $response = Invoke-WebRequest -Uri 'http://localhost:5656/get_applications' -Method GET
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json
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
            days_between = calc_days_between(created_date, modified_date)
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
                "status": app_dict.get("Status", "New"),
                "assignedRC": app_source.get("AssignedTo"),
                "daysInStage": days_between,
                "overdue": days_between > 10,
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
                stages =  [stage.to_dict() for stage in StageInstance.query.filter_by(ProcessInstanceId=process_instance.InstanceId).all()]
                if stages is None:
                    app_logger.warning(f"Stages not found for application id {application_id}")
                    return jsonify({"status": "error", "message": f"Workflow Stages not found for application id {application_id}"}), 404
                app_row["stages"] = {}
                for stage in stages:
                    tasks = []
                    task_cnt = 0
                    completed_cnt = 0
                    task_instances = TaskInstance.query.filter_by(StageId=stage['StageInstanceId']).all()
                    for task in task_instances:
                        if task.TaskDef.TaskType in ['START', 'END','GATEWAY','SUBPROCESS']:
                            continue
                        task_cnt += 1 if task.Status == 'Pending' else 0
                        completed_cnt += 1 if task.Status == 'Completed' else 0
                        created_date = task.StartedDate
                        modified_date = datetime.now() if task.Status != 'Completed' else task.get("CompletedDate")
                        days_between = calc_days_between(created_date, modified_date)
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
                                    { "taskRole": task.TaskDef.AssigneeRole if task and task.TaskDef else "Unknown Role" },
                                ],
                            }
                        )
                    lane = LaneDefinition.query.filter_by(LaneId=stage['LaneId']).first()
                    if lane:
                        lane_name = lane.to_dict()["LaneName"]
                        app_row["stages"].update({
                            lane_name: {
                                "status": stage["Status"] if task_cnt == 0 else "In Progress", 
                                "progress": completed_cnt / task_cnt  * 100 if  completed_cnt > 0 else 0,
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
                    "sender": msg.get("FromUser"), 
                    "text": msg.get("MessageText"),
                    "timestamp": msg.get("SentDate"),
                    "isSystemMessage": True if msg.get("MessageType") == "system" else False,
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