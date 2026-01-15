
from flask import app, request, jsonify, session
import logging
import safrs
from flask import request, jsonify
from flask_jwt_extended import  jwt_required
from database import models
from security.system.authorization import Security
from sqlalchemy import text
from datetime import datetime

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
                taskId = 540
                role = "NCRC"
                assignee = "admin"
            } | ConvertTo-Json

            Invoke-RestMethod -Uri "http://localhost:5656/assignRole" -Method POST -Body $body -ContentType "application/json" -Headers @{Authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1OTg2NDAyMSwianRpIjoiNzZhMjA3MWItOTY4Yi00NTAwLWEwYmMtYTcwN2Q0MDAyMmVhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzU5ODY0MDIxLCJleHAiOjE3NTk4NzczNDF9.s18ynSqujiwbylAnzH67nPKUFOW6ph_A1akM3PTM0u0"}
            

           curl -X 'POST' http://localhost:5656/assignRole -d '{"appId":1, "taskId":1, "role":"NCRC", "assignee":"S.Benjamin"}' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1ODIwMDg0MCwianRpIjoiNjY0MTNkYzItOWJhYi00NWI5LThkYzYtZTU1YjJkNjExN2Y1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzU4MjAwODQwLCJleHAiOjE3NTgyMTQxNjB9.0OCQKLwr-iSxnf62LRXtpd47Pb0wiHs6v72sI66ocz4'
        """


        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.get_json(force=True)
        app_id = data.get('appId')   # ApplicationID
        task_id = data.get('taskId')  # TaskInstanceId
        role = data.get('role')
        assignee = data.get('assignee')
        user = Security.current_user().Username
        access_token = request.headers.get('Authorization')
        if not data or 'appId' not in data or 'taskId' not in data or 'role' not in data or 'assignee' not in data:
            return jsonify({"error": "appId, taskId, role, and assignee are required"}), 400

        app_logger.info(f'Assign Role {role} to {assignee} for application {app_id} task {task_id}')
        # Here you would add the loigic to assign the role to the user for the application

        _assign_role(task_id, role, assignee, app_id, user, access_token)
        return jsonify({"result": f'Role {role} assigned to {assignee} for application {app_id} task {task_id}'}), 200

def _assign_role(task_id:int, role: str, assignee: str, app_id: int, user: str, access_token: str):
    """Assign role to user for the application.
    Args:
        role (str): The role to assign (e.g., 'NCRC', 'NCRCADMIN').
        assignee (str): The user to whom the role is assigned.
        app_id (int): The ID of the application.
    """
    
    try:
        #from api.api_discovery.complete_task_optimized import _complete_task_optimized as _complete_task
        from api.api_discovery.complete_task import _complete_task
       
        add_role_assignment(app_id, role, assignee, True)
        sql = get_admin_assitant(assignee)
        admin_assignee = session.execute(text(sql)).fetchone()
        if admin_assignee is None:
            admin_assignee = assignee 
        else:
            admin_assignee = admin_assignee.adminUserName
            #add_role_assignment(app_id, role, admin_assignee, False)
        
        # Remove assignment using  user roles - this is disabled for now
        roles = [] # Security.current_user().UserRoleList
        for this_role in roles:
            add_role_assignment(app_id, this_role.role_name, admin_assignee)

        session.commit()
        _complete_task(task_id, result='Assign Role', completed_by=user, completion_notes=f'Role {role} assigned to {assignee}', access_token=access_token)
    except Exception as e:
        session.rollback()
        app_logger.error(f'Error assigning role {role} to {assignee} for application {app_id}: {e}')
        raise Exception({"error": f"Failed to assign role {role} to {assignee} error: {e}"}, 500)
        # Set TaskInstance to Completed
    app_logger.info(f'TaskInstance set to Completed: {task_id}')
    

def add_role_assignment(application_id:int, role:str, assignee:str, isPrimary: bool = True):
    """Add a role assignment to the database.
    Args:
        application_id (int): The ID of the application.
        role (str): The role to assign (e.g., 'NCRC', 'NCRCADMIN').
        assignee (str): The user to whom the role is assigned.
    """
    existing_role =models.RoleAssigment.query.filter_by(
        ApplicationId=application_id,
        Role=role,
        Assignee=assignee
    ).first()
    if existing_role:
        app_logger.info(f'Role {role} already assigned to {assignee} for application {application_id}')
        #raise ValueError(f'Role {role} already assigned to {assignee} for application {application_id}') -- DO NOT THROW
        return
    role_assignment = models.RoleAssigment(
        ApplicationId=application_id,
        Role=role,
        Assignee=assignee,
        IsPrimary=isPrimary,
        CreatedDate=datetime.now()
    )
    session.add(role_assignment)
    session.commit()
    app_logger.info(f'Role {role} assigned to {assignee} for application {application_id}')

def get_admin_assitant(user:str):
    """Retrieve the admin assistant for a given user.
    Args:
        user (str): The username to look up.
    """
    return f"""
     SELECT  p.PERSON_ID , p.FIRST + '.' + p.LAST as 'NCRC'
         ,p.KashLogIn as NCRCuserName
         ,pa.PERSON_ID, pa.FIRST +'.' + pa.LAST as 'Admin'
        ,pa.KashLogIn as adminUserName
        FROM [ou_kash].[dbo].[PERSON_TB] p
          join [ou_kash].[dbo].person_job_tb pj on pj.PERSON_ID = p.PERSON_ID and pj.[FUNCTION] = 'NCRC'   and pj.ACTIVE=1      
          left join [ou_kash].[dbo].person_tb pa on pa.PERSON_ID = p.AdministrativeAssistant and pa.ACTIVE = 1
        where p.active = 1
            and p.LAST not like 'Z"%' and p.LAST <> 'Test' and p.first not like 'By R%'
            and p.KashLogIn = '{user}'
    """