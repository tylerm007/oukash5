from datetime import datetime
from email.mime import application
from database.models import LaneDefinition, WFApplicationMessage, WFFile, ProcessDefinition, ProcessInstance, TaskComment, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication
from flask import app, request, jsonify, session
import logging
import safrs
from flask import request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from safrs import jsonapi_rpc
from database import models

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass

    @app.route('/assignRole', methods=['OPTIONS','POST'])
    @jwt_required
    def assignRole():
        """        
            new custom end point to retrive admin for given ncrc
            post to assignRoles(appid, 'NCRC',user)
            post to assignRoles(appid, 'NCRCADMIN',retreivedadminuser)
            ({ appId, taskId, role, assignee }),

        Test it with:

           curl -X 'POST' http://localhost:5656/assignRole -d '{"applicationId":1, "role":"NCRC", "user":"S.Benjamin"}' -H 'accept: application/json' -H 'Authorization: Bearer <your_token>'
        """
        data = request.get_json()
        app_id = data.get('appId')   
        task_id = data.get('taskId')   
        role = data.get('role')
        assignee = data.get('assignee')
        if not data or 'appId' not in data or 'taskId' not in data or 'role' not in data or 'assignee' not in data:
            return jsonify({"error": "appId, taskId, role, and assignee are required"}), 400

        app_logger.info(f'Assign Role {role} to {assignee} for application {app_id} task {task_id}')
        # Here you would add the loigic to assign the role to the user for the application   
        application = models.WFApplication.query.filter_by(ApplicationID=app_id).first()
        if not application:
            return jsonify({"error": f"Application with ID {app_id} not found"}), 404
        task = models.TaskInstance.query.filter_by(TaskInstanceId=task_id).first()
        if not task:    
            return jsonify({"error": f"Task with ID {task_id} not found"}), 404
        application.AssignedTo = assignee
        application.AssignedDate = datetime.utcnow()
        application.Status = 'INP'
        session.add(application)
        session.commit()
         # Log the role assignment as a TaskComment 
        '''
        task_comment = TaskComment(
            TaskId=task_id,
            InstanceId=application.ProcessInstanceId,
            Action=f'Role {role} assigned to {assignee}',
            NewStatus='ROLE_ASSIGNED',
            ActionBy='system',
            ActionCommentText=f'Role {role} assigned to {assignee} for application {app_id}',
            ActionReason=f'Role {role} assigned to {assignee} for application {app_id}'
        )
        session.add(task_comment)
        session.commit()
        '''
        task.Status = 'COMPLETED'
        task.CompletedAt = datetime.utcnow()
        task.CompletedBy = 'system' 
        session.add(task)
        session.commit()
        app_logger.info(f'TaskInstance set to Completed: {task.TaskInstanceId}')
        return jsonify({"result": f'Role {role} assigned to {assignee} for application {app_id} task {task_id}'}), 200