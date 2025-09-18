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
    @jwt_required()
    def assignRole():
        """        
            new custom end point to retrive admin for given ncrc
            post to assignRoles(appid, 'NCRC',user)
            post to assignRoles(appid, 'NCRCADMIN',retreivedadminuser)
            ({ appId, taskId, role, assignee }),

        Test it with:

            $body = @{
                appId = 1
                taskId = 30
                role = "NCRC"
                assignee = "S.Benjamin"
            } | ConvertTo-Json

            Invoke-RestMethod -Uri "http://localhost:5656/assignRole" -Method POST -Body $body -ContentType "application/json" -Headers @{Authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1ODIxNzgxMCwianRpIjoiZTM3NzY2NTgtNmQyZS00MGNlLWJlMjEtM2QxNjE0NTU5NTQ3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzU4MjE3ODEwLCJleHAiOjE3NTgyMzExMzB9.JY3xPlkUddDIwvB1AYjO5ZiYUSyObxf7a-l9vAICe4Q"}
            

           curl -X 'POST' http://localhost:5656/assignRole -d '{"appId":1, "taskId":1, "role":"NCRC", "assignee":"S.Benjamin"}' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1ODIwMDg0MCwianRpIjoiNjY0MTNkYzItOWJhYi00NWI5LThkYzYtZTU1YjJkNjExN2Y1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzU4MjAwODQwLCJleHAiOjE3NTgyMTQxNjB9.0OCQKLwr-iSxnf62LRXtpd47Pb0wiHs6v72sI66ocz4'
        """
        data = request.get_json()
        app_id = data.get('appId')   
        task_id = data.get('taskId')   
        role = data.get('role')
        assignee = data.get('assignee')

        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
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
        task.CompletedDate = datetime.utcnow()
        session.add(task)
        session.commit()
        app_logger.info(f'TaskInstance set to Completed: {task.TaskInstanceId}')
        add_role_assignment(app_id, role, assignee)
        if role == 'NCRC':
            admin_assignee = assignee #TODO - how do we look up the admin for this NCRC?
            add_role_assignment(app_id, 'NCRCADMIN', admin_assignee)
        return jsonify({"result": f'Role {role} assigned to {assignee} for application {app_id} task {task_id}'}), 200
    
    def add_role_assignment(application_id, role, assignee):
        """Add a role assignment to the database.
        Args:
            application_id (int): The ID of the application.
            role (str): The role to assign (e.g., 'NCRC', 'NCRCADMIN').
            assignee (str): The user to whom the role is assigned.
        """
        role_assignment = models.RoleAssigment(
            ApplicationId=application_id,
            Role=role,
            Assignee=assignee,
            CreatedDate=datetime.utcnow()
        )
        session.add(role_assignment)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            app_logger.error(f'Error assigning role {role} to {assignee} for application {application_id}: {e}')
        else:
            app_logger.info(f'Role {role} assigned to {assignee} for application {application_id}')