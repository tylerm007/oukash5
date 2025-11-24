from datetime import datetime
from database.database_discovery.authentication_models import User
from security.system.authorization import Security
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
 
 
    @app.route('/get_application_tasks', methods=['GET','OPTIONS'])
    @app.route('/get_application_tasks_v1', methods=['GET','OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def get_application_tasks_v1():
 
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        from database.models import WFUser
        data = request.args if request.args else {}
        user = Security.current_user().Username
        app_logger.info(f"get_application_tasks called by user {user} with args: {data}")
        filter = data.get('filter', {})
        limit = int(data.get('page[limit]', 10))
        offset = int(data.get('page[offset]', 0))
        result = []
        args = request.args
        applicationId = args.get('filter[applicationId]', None) or args.get('applicationId', None)
        plantName = args.get('filter[plantName]', None) or args.get('plantName', None)
 
        params = {"userName": user,'applicationId': applicationId, 'plantName': plantName, 'limit': limit, 'offset': offset}

        app_logger.info(f"Calling dsql with: {params}")
        try:
            sql = get_SQL()
            tasks = session.execute(text(sql),params).fetchall()
 
        except Exception as e:
            app_logger.error(f"Error executing dsql: {e}")
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
        fields = tasks[0]._fields if len(tasks) > 0 else []
       
        # Convert tasks to dictionaries and add to result
        for task in tasks:
            task_dict = dict(zip(fields, task))
            result.append(task_dict)
       
        return jsonify({"status": "ok", "data": result}), 200
 
 
   
    def get_SQL() -> str:
       return '''
        SELECT  
        ap.[ApplicationID] as applicationId,
        ti.[TaskInstanceId] as taskInstanceId,
        td.[TaskName] as taskName,
        td.[Description] as taskDescription,
        td.[TaskType] as taskType,
        td.[TaskCategory] as TaskCategory,
        td.[AssigneeRole] as assigneeRole,
        ra.Assignee as assignee,
        ap.CompanyId as companyId,
        ap.PlantID as plantId,
        co.NAME as companyName,
        pl.NAME as plantName,
        ld.LaneName as stageName,
        ti.[Status] as status,
        ti.[StartedDate] as startedDate,
        ti.[CompletedDate] as completedDate,
        pi.InstanceId as processInstanceId,
        si.StageInstanceId as stageInstanceId,
        CASE
            WHEN ti.[CompletedDate] is not NULL THEN DATEDIFF(day,  ti.[StartedDate], ti.[CompletedDate] )
            ELSE  DATEDIFF(day, ti.[StartedDate], getdate())
        END as daysPending,
        CASE
            WHEN ti.[CompletedDate] is not NULL THEN null
            ELSE datediff(day, dateAdd(day,  (td.[EstimatedDurationMinutes] / 60 /24) , ti.[StartedDate]) ,  getdate())
        END as daysOverdue
    
    FROM [dashboard].[dbo].[TaskInstances] ti
        INNER JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
        INNER JOIN StageInstance si ON ti.StageId = si.StageInstanceId
        INNER JOIN ProcessInstances pi ON si.ProcessInstanceId = pi.InstanceId
        INNER JOIN WF_Applications ap ON pi.ApplicationId = ap.ApplicationID
        INNER JOIN LaneDefinitions ld ON si.LaneId = ld.LaneId
        LEFT JOIN ou_kash.dbo.plant_tb pl ON ap.plantID = pl.plant_ID
        LEFT JOIN ou_kash.dbo.COMPANY_TB co ON ap.companyId = co.COMPANY_ID
        INNER JOIN roleAssigment ra ON ra.Role = td.AssigneeRole AND ra.Assignee = :userName
        and ra.ApplicationId = ap.ApplicationID
    WHERE
        ap.status not in ('COMPL', 'WTH') AND
        ti.status = 'PENDING' AND
        (td.AssigneeRole != 'SYSTEM') AND
        (:applicationId IS NULL OR ap.ApplicationID = :applicationId) AND
        (:plantName IS NULL OR pl.Name like concat('%',:plantName,'%'))
        
    ORDER BY ap.applicationId, ti.taskInstanceId
    
        OFFSET :offset ROWS
        FETCH NEXT :limit ROWS ONLY
    '''