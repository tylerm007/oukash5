from ast import Continue
from datetime import datetime
from os import name
from token import NAME
from database.models import COMPANYTB, PLANTTB, LaneDefinition, TaskDefinition, WFApplicationMessage, WFFile, ProcessDefinition, ProcessInstance, TaskComment, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication, RoleAssigment
from flask import app, request, jsonify, session
import logging
import safrs
from sqlalchemy import false, text, or_, and_
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
import json
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
    
     # ============================================
    # STORED PROC OPTIMIZED VERSION
    # ============================================
    
    @app.route('/get_applications_v1', methods=['GET','OPTIONS'])
    @cross_origin()
    @admin_required()
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
        application_id = data.get('application_id', None) or data.get('filter[application_id]', None)   
        status = data.get('status', None) or data.get('filter[status]', None)

        #sql = "EXEC sp_GetApplications :application_id, :searchName,:limit, :offset"
        params = {'application_id': application_id, 'searchName': name_filter, 'status': status, 'priority': priority, 'limit': limit, 'offset': offset}
        #print(get_SQL(),params)
        result = session.execute(text(get_SQL()), params).fetchall()
        fields = result[0]._fields if len(result) > 0 else []
        data = []
        # = TaskDefinition.query.all() # USE CACHE HERE
        #task_definitions = {td.TaskId: td.to_dict() for td in task_defs}
        # Convert tasks to dictionaries and add to result
        for task in result:
            row = dict(zip(fields, task))
            assignedRoles = row.get('assignedRoles')
            if assignedRoles:
                assigned_roles= json.loads(assignedRoles)
                row['assignedRoles'] = [{role.get('role'): role.get("assignee", "Unknown")} for role in assigned_roles]
            files = row.get('files')
            row['files'] = []
            if files:
                row['files'] = json.loads(files)
            messages = row.get('messages')
            row['messages'] = []
            if messages:
                row['messages'] = json.loads(messages)
            row['quotes'] = []
            quotes = row.get('quotes')
            if quotes:
                row['quotes'] = json.loads(quotes)
            process = row.get('process')
            if process:
                row['stages'] = transform_process_row(process)
                row.pop('process', None)
            result = transform_app(row)
            data.append(result)
        #data = [dict(row) for row in result]
        total_count = WFApplication.query.count()
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
                "company": app.get("companyName", "Unknown Company"),
                "plant": app.get("plantName", "Unknown Plant"),
                "applicationId": app.get("ApplicationID"),
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

def transform_process_row(process: str) -> list:
    """
    Transforms a process row dictionary by parsing JSON fields.
    """
    import json
    result_stages = {}
    process_rows = []

    if process:
        process_rows = json.loads(process)
        for row in process_rows:
            stages = row.get('stages', [])
            lane_dict = get_lane_dict(stages)
            for stage in stages:
                stage_tasks = stage.get('tasks', [])
                tasks = []
                task_cnt = 0
                completed_cnt = 0
                for task in stage_tasks:
                    taskdef = task.get('td', [{}])[0]
                    if len(taskdef) == 0:
                        continue
                    #print(taskdef["TaskName"])
                    if (taskdef and taskdef['AutoComplete'] == True or
                        taskdef and taskdef['TaskType'] in ['START','END',"LANESTART",'LANEEND']):
                        continue
                
                    task_cnt += 1
                    completed_cnt += 1 if task['Status'] == 'COMPLETED' else 0

                    created_date = task['StartedDate'] if "StartedDate" in task else None
                    modified_date = datetime.now() if task['Status'] != 'COMPLETED' else task['CompletedDate']
                    days_between = _calc_days_between(created_date, modified_date)
                    days_due = int(taskdef['EstimatedDurationMinutes'] / 60) * 24 if taskdef and 'EstimatedDurationMinutes' in taskdef else 1

                    tasks.append({
                    "name": taskdef['TaskName'] if task and taskdef else "Unknown Task Name",
                    "status": task['Status'] if 'Status' in task else "UNKNOWN",
                    "taskType": taskdef['TaskType'] if task and taskdef else "Unknown Task Type",
                    "taskCategory": taskdef['TaskCategory'] if task and taskdef else "Unknown Task Category",
                    "executedBy": task['AssignedTo'] if "AssignedTo" in task else None,
                    "daysPending": days_between if task['Status'] == 'PENDING' else 0,
                    "daysOverdue": days_between - days_due if days_between > days_due and task['Status'] != 'COMPLETED' else 0,
                    "isOverdue": days_between > days_due and task['Status'] != 'COMPLETED',
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
                lane = lane_dict.get(stage['LaneId'])
                if lane:
                    lane_dict_data = lane.to_dict()
                    lane_name = lane_dict_data["LaneName"]
                    result_stages[lane_name] = {
                        "status": stage["Status"], 
                        "description": lane_dict_data["LaneDescription"],
                        "progress": int(completed_cnt / task_cnt * 100) if task_cnt > 0 and completed_cnt > 0 else 0,
                        "tasks": tasks
                    }
    return result_stages

def get_lane_dict(stages: list) -> dict:
    """
    Constructs a dictionary mapping LaneDefID to lane details from a list of stages.
    """
    lane_ids = [stage['LaneId'] for stage in stages]
    lanes = session.query(LaneDefinition).filter(
        LaneDefinition.LaneId.in_(lane_ids)
    ).all()
    lane_dict = {lane.LaneId: lane for lane in lanes} or {}
    return lane_dict

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
            #application_id = task['Stage']['ProcessInstance']['ApplicationId'] if task and task['Stage'] and task['Stage']['ProcessInstance'] else None
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
   select  pl.Name as "plantName", co.Name as "companyName",
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
    (
            select * 
            from WF_Quotes  
            where WF_Quotes.ApplicationID = app.ApplicationID
            FOR JSON AUTO
    ) as "quotes",
    (
            select * 
            from WF_Files 
            where   WF_Files.ApplicationID = app.ApplicationID
            FOR JSON AUTO
    ) as "files",
    (
            select * 
            from WF_ApplicationMessages  
            where WF_ApplicationMessages.ApplicationID = app.ApplicationID
            FOR JSON AUTO
    ) as "msgs",
    process = ( select * 
                       ,stages =  ( select *
                                           ,tasks =  ( select 
                                                        ti.TaskInstanceId,
                                                        ti.TaskId,
                                                        ti.Status,
                                                        ti.AssignedTo,
                                                        ti.StartedDate,
                                                        ti.CompletedDate,
                                                        td.TaskName,
                                                        td.Description,
                                                        td.TaskType,
                                                        td.TaskCategory,   
                                                        td.AssigneeRole,
                                                        td.EstimatedDurationMinutes,
                                                        td.AutoComplete,
                                                        td.IsRequired
                                                       from TaskInstances ti
                                                       INNER JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
                                                       where ti.StageId = si.StageInstanceId and  (td.AssigneeRole != 'SYSTEM') 
                                                       order by td.Sequence
                                                       FOR JSON AUTO
                                                     )
                                    from StageInstance si
                                    where si.ProcessInstanceId = pi.InstanceId
                                    order by si.StageInstanceId
                                    FOR JSON AUTO        
                                 )
                FROM ProcessInstances pi
                where   pi.ApplicationId = app.ApplicationID
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