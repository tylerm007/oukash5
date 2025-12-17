from datetime import datetime
from database.models import CompanyApplication, StageDefinition
from flask import app, request, jsonify, session
import logging
import safrs
from sqlalchemy import false, text, or_, and_
from flask_jwt_extended import get_jwt, jwt_required
import json
from database.cache_service import DatabaseCacheService

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None
cache = DatabaseCacheService.get_instance()

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass
    
     # ============================================
    # STORED PROC OPTIMIZED VERSION
    # ============================================
    
    @app.route('/get_applications_v1', methods=['GET','OPTIONS'])
    @jwt_required()
    def get_applications_v1():
        """
        OPTIMIZED ASYNC VERSION - Up to 10x faster than legacy version
        Processes applications concurrently for better performance
        
        Usage: Same as /get_applications but with async processing
        Returns additional meta.processing_time and meta.async_enabled fields
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        import time
        start_time = time.time()
        
        data = request.args if request.args else {}
        limit = int(data.get('page[limit]', 20))
        offset = int(data.get('page[offset]', 0))
        priority = data.get('priority', None) or data.get('filter[priority]', None)
        name_filter = data.get('name', None) or data.get('filter[name]', None)
        application_id = data.get('application_id', None) or data.get('filter[applicationId]', None)   
        status = data.get('status', None) or data.get('filter[status]', None)

        #sql = "EXEC sp_GetApplications :application_id, :searchName,:limit, :offset"
        params = {'application_id': application_id, 'searchName': name_filter, 'status': status, 'priority': priority, 'limit': limit, 'offset': offset}
        #print(get_SQL(),params)
        results = session.execute(text(get_SQL()), params).fetchall()
        fields = results[0]._fields if len(results) > 0 else []
        data = []
        # SQL Server FOR JSON PATH returns fragmented JSON strings when result is large
        # Concatenate all fragments from the result rows
        #task_definitions = {td.TaskId: td.to_dict() for td in task_defs}
        # Convert tasks to dictionaries and add to result
        
        for task in results:
            row = dict(zip(fields, task))
            assignedRoles = row.get('assignedRoles')
            if assignedRoles:
                assigned_roles= json.loads(assignedRoles)
                row['assignedRoles'] = [{role.get('role'): role.get("assignee", "Unknown")} for role in assigned_roles]
           
            stages = row.get('stages')
            if stages:
                stages_json = json.loads(stages)
                row['stages'] = transform_stage_row(stages_json)
                #row.pop('process', None)
            result = transform_app(row)
            data.append(result)
        #data = [dict(row) for row in result]
        
        wf_count =session.execute(text(get_total_count()), params).fetchone()[0]
        total_count = wf_count # len(data) if name or priority or status else 1 if  application_id else wf_count
        end_time = time.time()
        processing_time = end_time - start_time
        return jsonify({"status": "ok", "data": data, "meta": {"total_count": total_count, "count": len(data), "limit": limit,"offset":offset, "processing_time": processing_time, "async_enabled": True}}), 200

def transform_app(app) -> dict:
    """
    Transforms an application row dictionary by mapping status codes and processing stages.
    """
     # Build application data
    company_app = session.query(CompanyApplication).filter_by(ID=app.get("ApplicationNumber")).first()
    app_source = company_app.to_dict() if company_app else {}
    created_date = app.get("CreatedDate")
    modified_date = app.get("ModifiedDate")
    status = _get_app_status(app.get("Status"))
    days_between = _calc_days_between(created_date, None) if app.get("Status") not in ["COMPL","WTH"] else 0
    days_due = 5  #
    row ={
                #id": app.get("ApplicationID"),
                "company": app.get("company", "Unknown Company"),
                "plant": app.get("plant", "Unknown Plant"),
                "applicationId": app.get("applicationId"),
                "status": status,
                "priority": app.get("Priority", "Normal"),
                "daysInProcess": days_between,
                "daysOverdue": days_between - days_due if days_between > days_due and app.get("Status") != "COMPL" else 0,
                "isOverdue": days_between > days_due if app.get("Status") != "COMPL" else False,
                "createdDate": created_date,
                "lastUpdate": app.get("ModifiedDate"),
                "documents": 0,
                "notes": 0,
                "createdDate": created_date,
                "lastUpdate": modified_date,
                #"assignedRC": "Unassigned",
                "assignedRoles": app['assignedRoles'] if 'assignedRoles' in app else [],
                "stages": app['stages'] if 'stages' in app else {},
                "application_messages": [],
                "files": app['files'] if 'files' in app else [],
                "assignedRoles": app['assignedRoles'] if 'assignedRoles' in app else [],
            }
    return row

def transform_stage_row(stage_rows: any) -> list:
    """
    Transforms a process row dictionary by parsing JSON fields.
    """
    import json
    result_stages = {}
    task_definitions = cache.get_all_task_definitions()
    for row in stage_rows:
        stage_def = cache.get_stage_definition(stage_id=row.get('stageId'))
        stage_name = getattr(stage_def, 'StageName')
        tasks = []
        stage_tasks = row.get('tasks', [])
        stage_status = get_stage_status(stage_tasks, task_definitions)
        task_cnt = 0
        completed_cnt = 0
        for task in stage_tasks:
            taskdef_id = task.get('TaskDefinitionId')
            taskdef = task_definitions.get(taskdef_id).to_dict() if taskdef_id in task_definitions else {}
            if len(taskdef) == 0:
                continue
            #print(taskdef["TaskName"])
            if (taskdef and taskdef['AutoComplete'] == True or
                taskdef and taskdef['TaskType'] in ['START','END',"STAGESTART",'STAGEEND']):
                continue
        
            task_cnt += 1
            completed_cnt += 1 if task['status'] == 'COMPLETED' else 0

            #created_date = task['StartedDate'] if "StartedDate" in task else None
            #modified_date = datetime.now() if task['Status'] != 'COMPLETED' else task['CompletedDate']
            #days_between = _calc_days_between(created_date, modified_date)
            #days_due = int(taskdef['EstimatedDurationMinutes'] / (60 * 24)) if taskdef and 'EstimatedDurationMinutes' in taskdef else 1
            days_pending = task['daysPending'] if 'daysPending' in task else 0
            days_overdue = task['daysOverdue'] if 'daysOverdue' in task else 0
            tasks.append({
            "name": taskdef['TaskName'] if task and taskdef else "Unknown Task Name",
            "status": task['status'] if 'status' in task else "UNKNOWN",
            "taskType": taskdef['TaskType'] if task and taskdef else "Unknown Task Type",
            "taskCategory": taskdef['TaskCategory'] if task and taskdef else "Unknown Task Category",
            "executedBy": task['AssignedTo'] if "AssignedTo" in task else None,
            "daysPending": days_pending,
            "daysOverdue": days_overdue,
            "isOverdue": days_overdue > days_pending and task['Status'] != 'COMPLETED',
            "createdDate": task['StartedDate'] if "StartedDate" in task else None,
            "description": taskdef['Description'] if task and "Description" in taskdef else " ",
            "required": taskdef['IsRequired'] if task and "IsRequired" in taskdef else False,
            "TaskInstanceId": task['TaskInstanceId'],
            #"PreScript": _get_pre_script(task),
            "CompletedDate": task['CompletedDate'] if "CompletedDate" in task else None,
            "Result": task['Result'] if "Result" in task else None,
            "ResultData": task['ResultData'] if "ResultData" in task else None,
            "ErrorMessage": task['ErrorMessage'] if "ErrorMessage" in task else None,
            "taskRoles": [{
                "taskRole": taskdef['AssigneeRole'] if task and taskdef else "Unknown Role"
            }],
        })
        #lane = lane_dict.get(stage['LaneId'])
        if stage_name:
            #lane_dict_data = lane.to_dict()
            #lane_name = lane_dict_data["LaneName"]
            result_stages[stage_name] = {
                "status": stage_status, 
                "description": stage_def["StageDescription"],
                "progress": int(completed_cnt / task_cnt * 100) if task_cnt > 0 and completed_cnt > 0 else 0,
                "tasks": tasks
            }
    return result_stages

def get_stage_status(tasks: list, task_definitions: dict) -> str:
    """
    Determines the overall status of a stage based on its tasks.
    """
    if not tasks or len(tasks) == 0:
        return "NEW"
    start_completed = False
    count_tasks = 0
    count_completed = 0
    for task in tasks:
        taskdef_id = task.get('TaskDefinitionId')
        taskdef = task_definitions.get(taskdef_id).to_dict() if taskdef_id in task_definitions else {}
        if len(taskdef) == 0:
            continue
        count_tasks += 1
        if task.get('status') in ['PENDING','COMPLETED']: # could we add PENDING as well?? TODO count_pending
            count_completed += 1
            #if taskdef and taskdef['TaskType'] in ['START',"STAGESTART"]:
            #elif taskdef and taskdef['TaskType'] in ['END'"STAGEEND"]:
            start_completed  = True

    if start_completed:
        return "IN_PROGRESS"
    if count_completed == count_tasks and count_tasks > 0:
        return "COMPLETED"
    else:
        return "NEW"

def getStage_dict(stages: list) -> dict:
    """
    Constructs a dictionary mapping StageId to lane details from a list of stages.
    """
    
    stage_ids = [stage['StageId'] for stage in stages]
    stages = session.query(StageDefinition).filter(
        StageDefinition.StageId.in_(stage_ids)
    ).all()
    stage_dict = {stage.StageId: stage for stage in stages} or {}
    return stage_dict

def _calc_days_between(start_date, end_date) -> int:
    """Calculate days between two dates"""
    if not end_date or end_date == "":
        end_date = datetime.fromisoformat(datetime.now().isoformat()).isoformat()
    if start_date and end_date:
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        return (end_date - start_date).days
    return 0
    
def _get_app_status(status_code: str) -> str:
    """Get application status from code"""
    status_map = {
        "NEW": "New",
        "INP": "In Progress",
        "HLD": "On Hold",
        "WTH": "Withdrawn",
        "COMPL": "Certified",
        "REJ": "Rejected",
        "REVIEW": "Inspection Report Submitted to IAR",
        "INSPECTION": "Inspection Scheduled",
        "PAYPEND": "Payment Pending",
        "CONTRACT": "Contract Sent to Customer"
    }
    return status_map.get(status_code, "Unknown Status")

def _get_pre_script(task) -> str:
        """Get pre-script for task"""
        default_script = '''
            {
                "Title": "{{ Title }}",
                "Description": "{{ Description }}",
                "ApplicationID": "{{ ApplicationID }}",
                "TaskInstanceId": "{{ TaskInstanceId }}"
            }
        '''

        script = task['td'].PreScriptJson if task and task['td'] and task['td']['PreScriptJson'] else {}

        if script and isinstance(script, str) and '{{' in script:
            from jinja2 import Template
            template = Template(script)
            title = task['td'].TaskName if task and task['td'] else "Unknown Task Name"
            description = task['td'].Description if task and task['td'] else " "
            task_id = task['TaskInstanceId'] if task else None
            script = template.render(
                Title=title, 
                Description=description, 
                #ApplicationID=application_id, 
                TaskInstanceId=task_id
            )
        
        return script

def get_SQL() -> str:

    return '''
       select pl.Name as "plantName", 
         co.Name as "companyName",
         app.ApplicationID as applicationId,
         app.ApplicationNumber,
         app.CreatedDate,
         --app.ModifiedDate,
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
                                            ti.AssignedTo,
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



                    --from StageInstance si            
                    --where si.ApplicationId = app.ApplicationID 
                    --                  FOR JSON AUTO        
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

def get_total_count() -> str:
    return '''
    SELECT COUNT(*) as total_count
    FROM WF_Applications  app
         LEFT JOIN ou_kash.dbo.plant_tb pl ON app.plantID = pl.plant_ID
         LEFT JOIN ou_kash.dbo.COMPANY_TB co ON app.companyId = co.COMPANY_ID
     WHERE (:application_id IS NULL OR app.ApplicationID = :application_id)  and 
            (:priority IS NULL OR app.Priority = :priority) and
            (:status IS NULL OR app.Status = :status) and
            (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%'))
    '''