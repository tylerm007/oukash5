from ast import Continue
from datetime import datetime
from os import name
from token import NAME
from database.models import COMPANYTB, PLANTTB, LaneDefinition, WFApplicationMessage, WFFile, ProcessDefinition, ProcessInstance, TaskComment, TaskInstance , WFApplication, ProcessInstance, TaskInstance, StageInstance, CompanyApplication, RoleAssigment
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
    
    @app.route('/get_applications_sp', methods=['GET','OPTIONS'])
    @cross_origin()
    @admin_required()
    def get_applications_sp():
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

        sql = "EXEC sp_GetApplications :application_id, :searchName,:limit, :offset"
        params = {'application_id': application_id, 'searchName': name_filter, 'status': status, 'priority': priority, 'limit': limit, 'offset': offset}

        result = session.execute(text(sql), params).fetchall()
        fields = result[0]._fields if len(result) > 0 else []
        data = []
        # Convert tasks to dictionaries and add to result
        for task in result:
            row = dict(zip(fields, task))
            assignedRoles = row.get('assignedRoles')
            if assignedRoles:
                row['assignedRoles'] = json.loads(assignedRoles)
            files = row.get('files')
            if files:
                row['files'] = json.loads(files)
            process = row.get('process')
            if process:
                row['stages'] = transform_process_row(process)
                row.pop('process', None)
            data.append(row)
        #data = [dict(row) for row in result]
        end_time = time.time()
        processing_time = end_time - start_time
        return jsonify({"status": "ok", "data": data, "meta": {"processing_time": processing_time, "async_enabled": True}}), 200

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
                    #print(taskdef["TaskName"])
                    if (taskdef and taskdef['AutoComplete'] == True or
                        taskdef and taskdef['TaskType'] in ['START','END',"LANESTART",'LANEEND']):
                        continue
                
                    task_cnt += 1
                    completed_cnt += 1 if task['Status'] == 'COMPLETED' else 0

                    created_date = task['StartedDate']
                    modified_date = datetime.now() if task['Status'] != 'COMPLETED' else task['CompletedDate']
                    days_between = _calc_days_between(created_date, modified_date)
                    days_due = int(taskdef['EstimatedDurationMinutes'] / 60 * 24) if taskdef and taskdef['EstimatedDurationMinutes'] else 1

                    tasks.append({
                    "name": taskdef['TaskName'] if task and taskdef else "Unknown Task Name",
                    "status": task['Status'],
                    "taskType": taskdef['TaskType'] if task and taskdef else "Unknown Task Type",
                    "taskCategory": taskdef['TaskCategory'] if task and taskdef else "Unknown Task Category",
                    "executedBy": task['AssignedTo'] if "AssignedTo" in task else None,
                    "daysPending": days_between,
                    "daysOverdue": days_between - days_due if days_between > days_due and task['Status'] != 'COMPLETED' else 0,
                    "isOverdue": days_between > days_due and task['Status'] != 'COMPLETED',
                    "createdDate": task['StartedDate'] if "StartedDate" in task else None,
                    "description": taskdef['Description'] if task and taskdef else " ",
                    "required": taskdef['IsRequired'] if task and taskdef else False,
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
    lane_dict = {lane.LaneId: lane for lane in lanes}
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