from datetime import datetime, timedelta
from security.system.authorization import Security
from flask import app, request, jsonify, session
import logging
import safrs
from sqlalchemy import false, text
from flask_jwt_extended import get_jwt, jwt_required
 
app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session
_project_dir = None
 
def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass
 
 
    @app.route('/get_application_tasks', methods=['GET','OPTIONS'])
    @app.route('/get_application_tasks_v1', methods=['GET','OPTIONS'])
    @jwt_required()
    def get_application_tasks_v1():
 
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        data = request.args if request.args else {}
        username = Security.current_user().Username
        app_logger.info(f"get_application_tasks called by user {username} with args: {data}")
        filter = data.get('filter', {})
        limit = int(data.get('page[limit]', 50))
        offset = int(data.get('page[offset]', 0))
        application_type = data.get('applicationType', "WORKFLOW") or filter.get('applicationType',  "WORKFLOW") or  "WORKFLOW"
        result = []
        args = request.args
        applicationId = args.get('filter[applicationId]', None) or args.get('applicationId', None)
        plantName = args.get('filter[plantName]', None) or args.get('plantName', None)
        roles = ';'.join([f'{role.role_name}' for role in Security.current_user().UserRoleList])
        # Convert None to proper SQL NULL for pyodbc
        jwt = request.headers.get('Authorization', None)
        info = Security.extract_roles_and_delegated(jwt_token=jwt)
        delegated = info.get('delegated', None)
        days = args.get('filter[days]', None) or args.get('days', None)
        if delegated is not None:
            all_users = ";".join(delegated)
            all_users += f";{username}"
        params = {
            'username': all_users if delegated is not None else username,
            'applicationId': applicationId if applicationId else None,
            'plantName': plantName if plantName else None,
            'roles': roles if roles else None,
            'status': 'PENDING;IN_PROGRESS' if days is None else 'COMPLETED',
            'app_status': 'COMPL;WITH' if days is None else '',
            'completion_date': None if days is None else (datetime.now() - timedelta(days=int(days))).strftime('%Y-%m-%d'),
            'application_type': application_type,
            #'limit': limit,
            #'offset': offset
        }

        try:
            sql = get_SQL()
            app_logger.info(f"Calling dsql {sql} with params: {params}")
            # Execute with plain dict - let SQLAlchemy handle parameter expansion
            tasks = session.execute(text(sql), params).fetchall()
 
        except Exception as e:
            app_logger.error(f"Error executing dsql: {e}")
            return jsonify({"status": "error", "message": f"Database error: {str(e)}"}), 500
        fields = tasks[0]._fields if len(tasks) > 0 else []
       
        # Convert tasks to dictionaries and add to result
        for task in tasks:
            task_dict = dict(zip(fields, task))
            result.append(task_dict)
        #TODO - add StageInstance stuff back in Status, etc.
        meta = {'limit': limit, 'offset': offset, 'total': len(result)}
        return jsonify({"status": "ok", "data": result, "meta": meta}), 200
 
    def get_SQL()-> str:
        return '''
             SELECT  
            ap.[ApplicationID] as applicationId,
            ti.[TaskInstanceId] as taskInstanceId,
            td.[TaskName] as taskName,
            td.[Description] as taskDescription,
            td.[TaskType] as taskType,
            td.[TaskCategory] as TaskCategory,
            td.[AssigneeRole] as assigneeRole,
            td.PreScriptJson as PreScript,
            ra.Assignee as assignee,
            ap.CompanyId as companyId,
            ap.PlantID as plantId,
            co.NAME as companyName,
            pl.NAME as plantName,
            sd.StageName as stageName,
            ti.[Status] as status,
            ti.[StartedDate] as startedDate,
            ti.[CompletedDate] as completedDate,
            ti.[CompletedCapacity] as completedCapacity,
            ti.[CompletedBy] as completedBy,
            sd.StageId as stageInstanceId,
            1 as groupAssignment,
            CASE
                WHEN ti.[CompletedDate] is not NULL THEN DATEDIFF(day,  ti.[StartedDate], ti.[CompletedDate] ) 
                ELSE  DATEDIFF(day, ti.[StartedDate], getdate())
            END as daysPending,
            CASE
                WHEN ti.[CompletedDate] is not NULL THEN null 
                ELSE datediff(day, dateAdd(day,  (td.[EstimatedDurationMinutes] / 60 /24) , ti.[StartedDate]) ,  getdate())
            END as daysOverdue

            FROM TaskInstances ti
            INNER JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
            INNER JOIN WF_Applications ap ON ti.ApplicationId = ap.ApplicationID
            INNER JOIN StageDefinitions sd ON ti.stageId = sd.StageId
            LEFT JOIN ou_kash.dbo.plant_tb pl ON ap.plantID = pl.plant_ID
            LEFT JOIN ou_kash.dbo.COMPANY_TB co ON ap.companyId = co.COMPANY_ID
            INNER JOIN roleAssigment ra ON ra.Role = td.AssigneeRole 
                AND ra.Assignee = :username
                AND ra.ApplicationId = ap.ApplicationID
            WHERE 
            ap.status not in (SELECT value FROM STRING_SPLIT(:app_status, ';')) and
            (ap.ApplicationType = :application_type) and
            ti.status in (SELECT value FROM STRING_SPLIT(:status, ';')) AND 
            (td.AssigneeRole != 'SYSTEM') AND
            (:applicationId IS NULL OR ap.ApplicationID = :applicationId) and 
            (:plantName IS NULL OR pl.Name like concat('%',:plantName,'%'))
            and (:completion_date IS NULL OR ti.CompletedDate >= :completion_date)
            

            
            UNION ALL


            
            SELECT  
            ap.[ApplicationID] as applicationId,
            ti.[TaskInstanceId] as taskInstanceId,
            td.[TaskName] as taskName,
            td.[Description] as taskDescription,
            td.[TaskType] as taskType,
            td.[TaskCategory] as TaskCategory,
            td.[AssigneeRole] as assigneeRole,
            td.PreScriptJson as PreScript,
            'NULL' as assignee,
            ap.CompanyId as companyId,
            ap.PlantID as plantId,
            co.NAME as companyName,
            pl.NAME as plantName,
            sd.StageName as stageName,
            ti.[Status] as status,
            ti.[StartedDate] as startedDate,
            ti.[CompletedDate] as completedDate,
            ti.[CompletedCapacity] as completedCapacity,
            ti.[CompletedBy] as completedBy,
            sd.StageId as stageInstanceId,
            0 as groupAssignment,
            CASE
                WHEN ti.[CompletedDate] is not NULL THEN DATEDIFF(day,  ti.[StartedDate], ti.[CompletedDate] ) 
                ELSE  DATEDIFF(day, ti.[StartedDate], getdate())
            END as daysPending,
            CASE
                WHEN ti.[CompletedDate] is not NULL THEN null 
                ELSE datediff(day, dateAdd(day,  (td.[EstimatedDurationMinutes] / 60 /24) , ti.[StartedDate]) ,  getdate())
            END as daysOverdue

            FROM TaskInstances ti
            INNER JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
            INNER JOIN WF_Applications ap ON ti.ApplicationId = ap.ApplicationID
            INNER JOIN StageDefinitions sd ON ti.stageId = sd.StageId
            LEFT JOIN ou_kash.dbo.plant_tb pl ON ap.plantID = pl.plant_ID
            LEFT JOIN ou_kash.dbo.COMPANY_TB co ON ap.companyId = co.COMPANY_ID

            WHERE 
            td.AssigneeRole in (select RoleCode from TaskRoles where groupAssignment = 1) AND
            (ap.ApplicationType = :application_type) AND
            td.AssigneeRole IN (SELECT value FROM STRING_SPLIT(:roles, ';')) AND
            ap.status not in (SELECT value FROM STRING_SPLIT(:app_status, ';')) and
            ti.status in (SELECT value FROM STRING_SPLIT(:status, ';')) AND 
            (td.AssigneeRole != 'SYSTEM') AND
            (:applicationId IS NULL OR ap.ApplicationID = :applicationId) and 
            (:plantName IS NULL OR pl.Name like concat('%',:plantName,'%'))
            and (:completion_date IS NULL OR ti.CompletedDate >= :completion_date)
            
            ORDER BY ap.applicationId, ti.taskInstanceId
        '''

    def get_SQL_NEW() -> str:
        return '''
            SELECT  
                ap.[ApplicationID] as applicationId,
                ti.[TaskInstanceId] as taskInstanceId,
                td.[TaskName] as taskName,
                td.[Description] as taskDescription,
                td.[TaskType] as taskType,
                td.[TaskCategory] as TaskCategory,
                td.[AssigneeRole] as assigneeRole,
                td.PreScriptJson as PreScript,
                ap.CompanyId as companyId,
                ap.PlantID as plantId,
                co.NAME as companyName,
                pl.NAME as plantName,
                sd.StageName as stageName,
                ti.[Status] as status,
                ti.[StartedDate] as startedDate,
                ti.[CompletedDate] as completedDate,
                sd.StageId as stageInstanceId,
                CASE
                    WHEN ti.[CompletedDate] is not NULL THEN DATEDIFF(day,  ti.[StartedDate], ti.[CompletedDate] ) 
                    ELSE  DATEDIFF(day, ti.[StartedDate], getdate())
                END as daysPending,
                CASE
                    WHEN ti.[CompletedDate] is not NULL THEN null 
                    ELSE datediff(day, dateAdd(day,  (td.[EstimatedDurationMinutes] / 60 /24) , ti.[StartedDate]) ,  getdate())
                END as daysOverdue

            FROM TaskInstances ti
                INNER JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
                INNER JOIN WF_Applications ap ON ti.ApplicationId = ap.ApplicationID
                INNER JOIN StageDefinitions sd ON ti.stageId = sd.StageId
                LEFT JOIN ou_kash.dbo.plant_tb pl ON ap.plantID = pl.plant_ID
                LEFT JOIN ou_kash.dbo.COMPANY_TB co ON ap.companyId = co.COMPANY_ID
            WHERE 
                ap.status not in ('COMPL', 'WTH') AND
                -- Required filters
                ti.status = 'PENDING' AND 
                (td.AssigneeRole != 'SYSTEM') AND
                td.AssigneeRole IN (SELECT value FROM STRING_SPLIT(:roles, ';')) AND
                (:applicationId IS NULL OR ap.ApplicationID = :applicationId) AND
                (:plantName IS NULL OR pl.Name like concat('%',:plantName,'%'))
            
            ORDER BY ap.applicationId, ti.taskInstanceId
            OFFSET :offset ROWS
            FETCH NEXT :limit ROWS ONLY;
        '''
    
    # Removed StageInstance joins from V1
    def get_SQL_V1() -> str:
        return '''
            select pl.Name as "plantName", 
            co.Name as "companyName",
            app.ApplicationID,
            app.ApplicationNumber,
            app.CreatedDate,
            app.ModifiedDate,
            app.Status,
            app.Priority,
        (
                select role, assignee 
                from RoleAssigment  
                where RoleAssigment.ApplicationID = app.ApplicationID
                FOR JSON AUTO
        ) as "assignedRoles",

                
        
        stages =  ( select  sd.stageName
                            ,sd.stageId
                            ,sd.StageDescription
                            
                
                            ,tasks =  ( select 
                                            ti.TaskInstanceId,
                                            ti.TaskDefinitionId,
                                            ti.status,
                                            ti.TaskRole,
                                            ti.CompletedBy,
                                            ti.StartedDate,
                                            ti.CompletedDate,
                                            CASE
                                                                WHEN ti.status = 'PENDING' and  ti.[CompletedDate] is NULL THEN DATEDIFF(day,  ti.[StartedDate], getdate() ) 
                                                                ELSE NULL
                                            END as daysPending,
                                            CASE
                                                                WHEN ti.status = 'PENDING' and  ti.[CompletedDate] is NULL THEN 
                                                                    DATEDIFF(day, dateAdd(day,  (td.[EstimatedDurationMinutes] / 60 /24) , ti.[StartedDate]) ,  getdate())
                                                                ELSE NULL
                                            END as daysOverdue
                                        from TaskInstances ti
                                                INNER JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
                                                            where ti.StageId = sd.StageId and  (td.AssigneeRole != 'SYSTEM') 
                                                            FOR JSON AUTO
                                    )
                    from TaskInstances ti 
                    LEFT JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
                    LEFT JOIN StageDefinitions sd ON ti.stageId = sd.StageId
                    where ti.ApplicationId = app.ApplicationID  and td.AssigneeRole != 'SYSTEM'
                    group by sd.stageName, sd.stageId, StageDescription
                    FOR JSON AUTO     
                    )
                
                            
                FROM WF_Applications  app
                    LEFT JOIN ou_kash.dbo.plant_tb pl ON app.plantID = pl.plant_ID
                    LEFT JOIN ou_kash.dbo.COMPANY_TB co ON app.companyId = co.COMPANY_ID
                
                WHERE (:application_id IS NULL OR app.ApplicationID = :application_id)  and 
                        (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%'))
                

                ORDER BY app.ApplicationID   
                OFFSET :offset ROWS
                FETCH NEXT :limit ROWS ONLY;
        '''
    # This is for dashboard - removing StageInstance above
    def get_SQL_V1() -> str:
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
            sd.StageName as stageName,
            ti.[Status] as status,
            ti.[StartedDate] as startedDate,
            ti.[CompletedDate] as completedDate,
            --pi.InstanceId as processInstanceId,
            si.StageInstanceId as stageInstanceId,
            CASE
                WHEN ti.[CompletedDate] is not NULL THEN DATEDIFF(day,  ti.[StartedDate], ti.[CompletedDate] ) 
                ELSE  DATEDIFF(day, ti.[StartedDate], getdate())
            END as daysPending,
            CASE
                WHEN ti.[CompletedDate] is not NULL THEN null 
                ELSE datediff(day, dateAdd(day,  (td.[EstimatedDurationMinutes] / 60 /24) , ti.[StartedDate]) ,  getdate())
            END as daysOverdue

        FROM TaskInstances ti
            INNER JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
            INNER JOIN StageInstance si ON ti.StageId = si.StageInstanceId
            INNER JOIN WF_Applications ap ON si.ApplicationId = ap.ApplicationID
            INNER JOIN StageDefinitions sd ON si.stageDefinitionId = sd.StageId
            LEFT JOIN ou_kash.dbo.plant_tb pl ON ap.plantID = pl.plant_ID
            LEFT JOIN ou_kash.dbo.COMPANY_TB co ON ap.companyId = co.COMPANY_ID
            INNER JOIN roleAssigment ra ON ra.Role = td.AssigneeRole AND ra.Assignee = :userName 
            and ra.ApplicationId = ap.ApplicationID
        WHERE 
            ap.status not in ('COMPL', 'WTH') and
            -- Required filters 
            ti.status = 'PENDING' AND 
            (td.AssigneeRole != 'SYSTEM') AND
            (:applicationId IS NULL OR ap.ApplicationID = :applicationId) and 
        (:plantName IS NULL OR pl.Name like concat('%',:plantName,'%'))
        
        ORDER BY ap.applicationId, ti.taskInstanceId
    
    '''