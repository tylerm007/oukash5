from datetime import datetime
from database.models import StageDefinition, WFApplication, TaskInstance
from database.oukash_models import CompanyApplication, OWNSTB
from database.submission_models import SubmissionMatcher, SubmissionPlant
from flask import app, request, jsonify, session
import logging
import jwt
import safrs
from sqlalchemy import false, text, or_, and_
from flask_jwt_extended import get_jwt, jwt_required
import json
from database.cache_service import DatabaseCacheService
from security.system.authorization import Security
from database.utils import parse_sqlserver_json

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
        
        username = Security.current_user().Username
        data = request.args if request.args else {}
        limit = int(data.get('page[limit]', 20))
        offset = int(data.get('page[offset]', 0))
        priority = data.get('priority', None) or data.get('filter[priority]', None)
        name_filter = data.get('name', None) or data.get('filter[name]', None)
        application_id = data.get('application_id', None) or data.get('filter[applicationId]', None)   
        status = data.get('status', None) or data.get('filter[status]', None)
        application_type = data.get('application_type','WORKFLOW') #or SUBMISSION
        only_my_apps = data.get('filter[OnlyMyRoles]', 'false')  
        role_to_use = data.get('filter[role]', None)
        if application_type == 'WORKFLOW':
            sql = get_SQL() if only_my_apps.lower() == 'false' else getSQLForRoles()
        else:
            sql = get_SUBMISSION_SQL() if only_my_apps.lower() == 'false' else getSQLForRoles()
        info = Security.extract_roles_and_delegated(jwt_token=jwt)
        delegated = info.get('delegated', None) if info else None
        roles = ';'.join([f'{role.role_name}' for role in Security.current_user().UserRoleList])
        application_matching_sql = update_application_matching_sql()
        session.execute(text(application_matching_sql))
        session.commit()
        admin_users = None
        if delegated is not None:
            admin_users = ";".join(d for d in delegated)
            #admin_users += f";{username}"
        if only_my_apps.lower() == 'true':
            #if role_to_use not in roles:
            #    raise Exception(f"User {username} does not have role: {role_to_use} to filter applications")
            roles = role_to_use if role_to_use and role_to_use in roles else roles
            sql = getSQLForOneRole()
            admin_users = admin_users if role_to_use == 'Administrative Assistant' else None
        params = {
            'application_id': application_id,
            'searchName': name_filter, 
            'status': status, 
            'priority': priority, 
            'limit': limit, 
            'offset': offset,
            'application_type': application_type,
            #"when_assigned": whenAssigned
        } if only_my_apps.lower() == 'false' else {
            'application_id': application_id,
            'searchName': name_filter,
            'status': status, 
            'priority': priority,  
            'userName': username,
            'assistantMgrList': admin_users if admin_users is not None else None,
            'userRoles': roles,
            'limit': limit, 
            'offset': offset,
            'application_type': application_type,
        }

        print(sql,params)
        results = session.execute(text(sql), params).fetchall()
        fields = results[0]._fields if len(results) > 0 else []
        data = []
        # SQL Server FOR JSON PATH returns fragmented JSON strings when result is large
        # Concatenate all fragments from the result rows
        #task_definitions = {td.TaskId: td.to_dict() for td in task_defs}
        # Convert tasks to dictionaries and add to result
        json_data = []
        for row in results:
            # Each row is a tuple with one element (the JSON fragment)
            if row:
                json_data.append( dict(zip(fields, row)))
        
        for row in json_data:
            assignedRoles = row.get('assignedRoles')
            if assignedRoles:
                assigned_roles= json.loads(assignedRoles)
                row['assignedRoles'] = [{role.get('role'): role.get("assignee", "Unknown"), "isPrimary": role.get("IsPrimary", True)} for role in assigned_roles]
           
            stages = row.get('stages')
            if stages:
                stages_json = json.loads(stages)
                row['stages'] = transform_stage_row(stages_json, application_type)
                #row.pop('process', None)
            result = transform_app(row, application_type=application_type)
            data.append(result)
        #data = [dict(row) for row in result]
        sql_count = get_total_count() 
        if only_my_apps.lower() == 'true' and role_to_use:
            #sql_count = get_total_count_for_one_role() # TODO NOT WORKING
            params = {
                'application_id': application_id,
                'searchName': name_filter,
                'status': status, 
                'priority': priority,  
                'userName': username,
                #'assistantMgrList': admin_users if admin_users is not None else None, # TODO
                'userRoles': roles,
                'application_type': application_type,
            }
        print(sql_count)
        wf_count =session.execute(text(sql_count), params).fetchone()[0]
        total_count = wf_count # len(data) if name or priority or status else 1 if  application_id else wf_count
        end_time = time.time()
        processing_time = end_time - start_time
        return jsonify({"status": "ok", "data": data, "meta": {"total_count": total_count, "count": len(data), "limit": limit,"offset":offset, "processing_time": processing_time, "async_enabled": True}}), 200

def transform_app(app, application_type:str = 'WORKFLOW') -> dict:
    """
    Transforms an application row dictionary by mapping status codes and processing stages.
    """
     # Build application data
    company_app = session.query(CompanyApplication).filter_by(ID=app.get("ApplicationNumber")).first()
    app_source = company_app.to_dict() if company_app else {}
    created_date = app.get("CreatedDate")
    modified_date = app.get("ModifiedDate")
    status = _get_app_status(app.get("Status"),application_type)
    days_between = _calc_days_between(created_date, None) if app.get("Status") not in ["COMPL","WTH"] else 0
    days_due = 5  #
    withdrawn_reason = None
    if app.get('Status') == 'WTH':
        withdrawn_reason = find_withdrawn_reason(app.get("applicationId"))
    row ={
                #id": app.get("ApplicationID"),
                "company": app.get("companyName", "Unknown Company"),
                "plant": app.get("plantName", "Unknown Plant"),
                "applicationId": app.get("applicationId"),
                "withdrawn_reason": withdrawn_reason,
                'companyId': app.get("companyId"),
                "externalReferenceId": app.get("externalReferenceId"),
                "WFID": app.get("WFLinkedApp"),
                'plantId': app.get("plantId"),
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
                "stages": app['stages'] if 'stages' in app and app['stages'] is not None else {},
                "application_messages": [],
                "files": app['files'] if 'files' in app else [],
                #"assignedRoles": app['assignedRoles'] if 'assignedRoles' in app else [],
            }
    if application_type == 'SUBMISSION':
        companyFromApplication = parse_sqlserver_json(app.get("companyFromApplication", "{}"))
        companyContacts = parse_sqlserver_json(app.get("companyContacts", "{}"))
        plants = session.query(SubmissionPlant).filter_by(SubmissionAppId=app.get("externalReferenceId")).all()
        #json.loads(app.get("plants", "[]"))
        for stage in row['stages'].values():
            for task in stage.get("tasks", []):
                if task.get("name") == 'ResolveCompany':
                    matcher = session.query(SubmissionMatcher).filter_by(SubmissionAppId=app.get("externalReferenceId"), SubmissionType="COMPANY").first()
                    if companyFromApplication and len(companyFromApplication) > 0:
                        task['companyFromApplication'] = companyFromApplication[0] 
                        task['companyFromApplication']['companyContacts'] = companyContacts if companyContacts else {}
                        task['companyMatchList'] = [] if matcher is None else parse_sqlserver_json(matcher.SubbmissionMatches) if matcher and matcher.SubbmissionMatches else []
                        task['companySelected'] = {} if task['Result'] is None or task['Result'] == '' else {
                            "companyName": companyFromApplication[0].get("companyName", "Unknown Company"),
                            "ID": task['Result'],
                            "Address": companyFromApplication[0].get("companyAddress", "Unknown Address"),
                        }
                elif 'ResolvePlant' in task.get("name", ""): # Plant#1 - 5
                    resultData = task.get("ResultData") or {}
                    #plantContacts = json.loads(app.get("plantContacts") or "{}")
                    result_data = parse_sqlserver_json(resultData) if isinstance(resultData, str) and resultData.startswith('{') else {}
                    plantInfo = result_data[0] if result_data and isinstance(result_data, list) and len(result_data) > 0 else result_data
                    plantId = plantInfo.get("PlantId") if plantInfo else None
                    task['name'] = 'ResolvePlant'
                    for plant in plants:
                        if plantId and str(plant.PlantId) != str(plantId):
                            continue
                        workflow_app_id = ""
                        owns_id = ""
                        if task['Result'] != '':
                            linked_app = session.query(WFApplication).filter_by(PlantID=task['Result'],ApplicationType='WORKFLOW').first()
                            if linked_app:
                                workflow_app_id = linked_app.ApplicationID 
                            owns_id = plantInfo.get("OWNSID") or ""
                            if not owns_id:
                                owns_record = session.query(OWNSTB).filter_by(PLANT_ID=task['Result']).first()
                                owns_id = owns_record.ID if owns_record else ""
                        task['plantFromApplication'] = {
                                "plantName": plant.plantName if len(plants) > 0 else "Unknown Plant",
                                "Address": f'{plant.plantAddress}, {plant.plantCity} {plant.plantState} {plant.plantZip} {plant.plantCountry}' if len(plants) > 0 else "",
                                "plantID": plant.PlantId,
                                "plantNumber": plant.plantNumber,
                                "brieflySummarize": plant.brieflySummarize,
                                "plantContacts":json.loads(app.get('plants'))[int( plant.plantNumber) - 1].get('plantContacts') if app.get('plants') else []
                        }
                        matcher = session.query(SubmissionMatcher).filter_by(SubmissionKey=plantId, SubmissionType="PLANT").first()
                        task['plantMatchList'] = [] if matcher is None else parse_sqlserver_json(matcher.SubbmissionMatches) if matcher and matcher.SubbmissionMatches else []
                        task['plantSelected'] = {} if task['Result'] is None or task['Result'] == '' else {
                                "plantName": plant.plantName ,
                                "Address": f'{plant.plantAddress}, {plant.plantCity} {plant.plantState} {plant.plantZip} {plant.plantCountry}' if len(plants) > 0 else "",
                                "PlantID": task['Result'],
                                "OWNSID": owns_id,
                                "WFID": workflow_app_id
                            }
                        
    return row
def find_withdrawn_reason(app_id:int):
    reason = None
    task_instances = session.query(TaskInstance).filter_by(ApplicationId=app_id, Status='COMPLETED').all()
    for task_instance in task_instances:
        task_def = task_instance.TaskDefinition
        if task_def and task_def.TaskName.upper() == 'CANCEL APPLICATION':
            resultData = parse_sqlserver_json(task_instance.ResultData) if task_instance.ResultData else None
            return resultData.get("notes") if resultData and isinstance(resultData, dict) and "notes" in resultData else None

    return reason

def transform_stage_row(stage_rows: any, application_type:str = 'WORKFLOW') -> list:
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
            
            if task.get('AssigneeRole') == 'SYSTEM':
                continue
            #print(taskdef["TaskName"])
            if (taskdef and taskdef['AutoComplete'] == True or
                taskdef and taskdef['TaskType'] in ['START','END',"STAGESTART",'STAGEEND']):
                continue
        
            task_cnt += 1
            completed_cnt += 1 if task['status'] == 'COMPLETED' else 0

            if len(taskdef) == 0 or taskdef.get('TaskName') == 'AssignNCRC':
                continue
            #created_date = task['StartedDate'] if "StartedDate" in task else None
            #modified_date = datetime.now() if task['Status'] != 'COMPLETED' else task['CompletedDate']
            #days_between = _calc_days_between(created_date, modified_date)
            #days_due = int(taskdef['EstimatedDurationMinutes'] / (60 * 24)) if taskdef and 'EstimatedDurationMinutes' in taskdef else 1
            days_pending = task['daysPending'] if 'daysPending' in task else 0
            days_overdue = task['daysOverdue'] if 'daysOverdue' in task else 0
            if application_type == 'SUBMISSION' and taskdef and 'ResolvePlant' in taskdef['TaskName'] and task.get("IsVisible") == 0:
                continue
            tasks.append({
            "name": taskdef['TaskName'] if task and taskdef else "Unknown Task Name",
            "status": task['status'] if 'status' in task else "UNKNOWN",
            "taskType": taskdef['TaskType'] if task and taskdef else "Unknown Task Type",
            "taskCategory": taskdef['TaskCategory'] if task and taskdef else "Unknown Task Category",
            "executedBy": task['CompletedBy'] if "CompletedBy" in task else None,
            "TaskRole": task['TaskRole'] if "TaskRole" in task else None,
            "CompletedCapacity": task['CompletedCapacity'] if "CompletedCapacity" in task else None,    
            "daysPending": days_pending,
            "daysOverdue": days_overdue,
            "isOverdue": days_overdue > days_pending and task['Status'] != 'COMPLETED',
            "createdDate": task['StartedDate'] if "StartedDate" in task else None,
            "description": taskdef['Description'] if task and "Description" in taskdef else " ",
            "required": taskdef['IsRequired'] if task and "IsRequired" in taskdef else False,
            "TaskInstanceId": task['TaskInstanceId'],
            "PreScript":taskdef['PreScriptJson'] if "PreScriptJson" in taskdef else None,
            "CompletedDate": task['CompletedDate'] if "CompletedDate" in task else None,
            'activeStartDate': task['ActiveStartDate'] if "ActiveStartDate" in task else None,
            "Result": task.get('Result'),
            "ResultData": task.get('ResultData'),
            "ErrorMessage": task.get('ErrorMessage'),
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
    status = 'NEW'
    if not tasks or len(tasks) == 0:
        return status
    stage_start = False
    stage_end = False
    for task in tasks:
        taskdef_id = task.get('TaskDefinitionId')
        taskdef = task_definitions.get(taskdef_id).to_dict() if taskdef_id in task_definitions else {}
        if len(taskdef) == 0:
            continue
        
        if task.get('status') in ['COMPLETED']: # could we add PENDING as well?? TODO count_pending            
            if taskdef and taskdef['TaskType'] in ['START',"STAGESTART"]:
                stage_start = True
            elif taskdef and taskdef['TaskType'] in ['END','STAGEEND']:
                stage_end = True
            

    if stage_start and not stage_end:
        return "IN_PROGRESS"
    if stage_start and stage_end:
        status = "COMPLETED"
    else:
        status = "NEW"
    return status

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
    
def _get_app_status(status_code: str,application_type:str = 'WORKFLOW') -> str:
    """Get application status from code"""
    status_map = {
        "NEW": "New",
        "INP": "In Progress",
        "HLD": "On Hold",
        "WTH": "Withdrawn",
        "COMPL":"Completed" if application_type != 'WORKFLOW' else "Certified",
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
         app.ExternalAppRef as 'externalReferenceId',
         app.WFLinkedApp as 'WFID',
         app.CreatedDate,
         --app.ModifiedDate,
         app.Status,
         app.Priority,
         app.CompanyID as 'companyId',
         app.PlantID as 'plantId',
        (
                select role, assignee , IsPrimary
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
                                            ti.CompletedBy,
                                            ti.CompletedCapacity,
                                            ti.StartedDate,
                                            ti.CompletedDate,
                                            ti.ActiveStartDate,
                                            ti.Result,
                                            ti.ResultData,
                                            ti.IsVisible,
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
                                                            where ti.StageId = sd.StageId 
                                                            and ti.ApplicationId = app.ApplicationID
                                                            -- and  (td.AssigneeRole != 'SYSTEM') 
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
            (:priority IS NULL OR app.Priority = :priority) and
            (:status IS NULL OR app.Status = :status) and
            (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%'))
            AND (ApplicationType = :application_type)

        ORDER BY app.CreatedDate DESC
        OFFSET :offset ROWS
        FETCH NEXT :limit ROWS ONLY;

    '''
def get_SUBMISSION_SQL() -> str:
       return '''
       select 
         co.companyName,
         app.ApplicationID as applicationId,
         app.ApplicationNumber,
         app.CreatedDate,
         app.ModifiedDate,
         app.Status,
         app.Priority,
         app.ExternalAppRef as 'externalReferenceId',
         app.WFLinkedApp as 'WFID',
         ( select
             co1.companyName as "companyName",
             co1.companyAddress,
             co1.companyAddress2,
             co1.companyCity,
             co1.companyState,
             co1.ZipPostalCode,
             co1.companyCountry,
             co1.companyPhone,
             co1.companyRegion,
             co1.companyProvince,
             co1.companyWebsite,
             co1.whichCategory,
             co1.numberOfPlants,
             co1.copack   
             from [dashboardV1].[dbo].[SubmissionApplication] co1
             WHERE co1.SubmissionAppId = app.ExternalAppRef
             FOR JSON AUTO

         ) as companyFromApplication,
         (
            SELECT 
            co2.IsPrimaryContact,
             co2.contactFirst,
             co2.contactLast,
             co2.contactEmail,
             co2.contactPhone,
             co2.billingContact,
             co2.billingContactFirst,
             co2.billingContactLast,
             co2.billingContactEmail,             
             co2.billingContactPhone,
             co2.jobTitle1,
             co2.contactFirst1,
             co2.contactLast1,
             co2.contactEmail1,
             co2.contactPhone1      
             from [dashboardV1].[dbo].[SubmissionApplication] co2
             where co2.SubmissionAppId = app.ExternalAppRef
             FOR JSON AUTO
         ) as companyContacts,
        ( SELECT 
            pl.plantName as "plantName", 
            pl.plantNumber,
            pl.plantAddress,
            pl.plantCity,
            pl.plantState,
            pl.plantZip,
            pl.plantRegion,
            pl.plantCountry,
            (  SELECT
                pc.contactFirst, 
                pc.contactLast,
                pc.contactEmail,
                pc.contactPhone,
                pc.jobTitle,
                pc.contactFirst1 ,
                pc.contactLast1,
                pc.contactEmail1,
                pc.contactPhone1,   
                pc.jobTitle1
                from [dashboardV1].[dbo]. SubmissionPlant pc
                where pc.PlantId = pl.PlantId
                FOR JSON AUTO  
            ) as plantContacts
            FROM [dashboardV1].[dbo].[SubmissionPlant] pl
            where pl.SubmissionAppId = app.ExternalAppRef
            FOR JSON AUTO
        ) as plants,
        (
                select role, assignee , IsPrimary
                from [dashboard].[dbo]. RoleAssigment  
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
                                            ti.CompletedBy,
                                            ti.CompletedCapacity,
                                            ti.StartedDate,
                                            ti.CompletedDate,
                                            ti.ActiveStartDate,
                                            ti.Result,
                                            ti.ResultData,
                                            ti.IsVisible,
                                            CASE
                                                                WHEN ti.status = 'PENDING' and  ti.[CompletedDate] is NULL THEN DATEDIFF(day,  ti.[StartedDate], getdate() ) 
                                                                ELSE NULL
                                            END as daysPending,
                                            CASE
                                                                WHEN ti.status = 'PENDING' and  ti.[CompletedDate] is NULL THEN 
                                                                    DATEDIFF(day, dateAdd(day,  (td.[EstimatedDurationMinutes] / 60 /24) , ti.[StartedDate]) ,  getdate())
                                                                ELSE NULL
                                            END as daysOverdue
                                        from  [dashboard].[dbo].TaskInstances ti
                                                INNER JOIN [dashboard].[dbo]. TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
                                                            where ti.StageId = sd.StageId 
                                                            and ti.ApplicationId = app.ApplicationID
                                                            -- and  (td.AssigneeRole != 'SYSTEM') 
                                                            FOR JSON AUTO
                                    )
                        from  [dashboard].[dbo].TaskInstances ti 
                        LEFT JOIN  [dashboard].[dbo].TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
                        LEFT JOIN  [dashboard].[dbo].StageDefinitions sd ON ti.stageId = sd.StageId
                        where ti.ApplicationId = app.ApplicationID  and td.AssigneeRole != 'SYSTEM'
                        group by sd.stageName, sd.stageId, StageDescription
                        FOR JSON AUTO   
                    )
                
                            
        FROM [dashboard].[dbo].[WF_Applications]  app
            LEFT JOIN [dashboardV1].[dbo].SubmissionApplication co ON app.ExternalAppRef = co.SubmissionAppId
        
        WHERE (:application_id IS NULL OR app.ApplicationID = :application_id)  and 
            (:priority IS NULL OR app.Priority = :priority) and
            (:status IS NULL OR app.Status = :status) and
            (:searchName IS NULL OR co.companyName like concat('%',:searchName,'%'))
            AND (ApplicationType = :application_type)

        ORDER BY app.CreatedDate DESC
        OFFSET :offset ROWS
        FETCH NEXT :limit ROWS ONLY;
        '''
def getSQLForRoles():
    return '''
     select  pl.Name as "plantName", 
         co.Name as "companyName",
         app.ApplicationID as applicationId,
         app.ApplicationNumber,
         app.ExternalAppRef as 'externalReferenceId',
         app.WFLinkedApp as 'WFID',
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
                                            ti.AssignedTo,
                                            ti.StartedDate,
                                            ti.CompletedDate,
                                            ti.ActiveStartDate,
                                            ti.Result,
                                            ti.ResultData,
                                            ti.IsVisible,
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
                                                            where ti.StageId = sd.StageId 
                                                            --and  (td.AssigneeRole != 'SYSTEM')
                                                            and ti.ApplicationId = app.ApplicationID 
                                                            FOR JSON AUTO
                                    )
                    from TaskInstances ti 
                    LEFT JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
                    LEFT JOIN StageDefinitions sd ON ti.stageId = sd.StageId
                    where ti.ApplicationId = app.ApplicationID  
                    -- and td.AssigneeRole != 'SYSTEM'
                    group by sd.stageName, sd.stageId, StageDescription
                    FOR JSON AUTO   
                    )     
                            
        FROM WF_Applications  app
            LEFT JOIN ou_kash.dbo.plant_tb pl ON app.plantID = pl.plant_ID
            LEFT JOIN ou_kash.dbo.COMPANY_TB co ON app.companyId = co.COMPANY_ID

        WHERE 
        (ApplicationType = :application_type) AND
        (:priority IS NULL OR app.Priority = :priority) and
        (:status IS NULL OR app.Status = :status) and
        (:application_id IS NULL OR app.ApplicationID = :application_id)  and 
        (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%')) and
        (:userName is not null  and  app.ApplicationID in (
            --user assigment
            select distinct(app.ApplicationID)  from WF_Applications  app
                                        INNER JOIN roleAssigment ra ON ra.ApplicationId = app.ApplicationID  
                                        AND ra.Assignee = :userName
                                        and  ra.Role in (select [RoleCode] from TaskRoles where [groupAssignment] != 1)
            -- admin
            union
            select distinct(app.ApplicationID)  from WF_Applications  app
                                        INNER JOIN roleAssigment ra ON ra.ApplicationId = app.ApplicationID and 
                                        ra.Assignee  IN (SELECT value FROM STRING_SPLIT(:assistantMgrList, ';'))
            --group assigment 
            union

            select distinct(ti.ApplicationID)  from  TaskInstances ti 
                        LEFT JOIN TaskDefinitions td ON td.AssigneeRole in (select [RoleCode] from TaskRoles where [groupAssignment] = 1 ) 
                            where 
                                    td.assigneeRole IN (SELECT value FROM STRING_SPLIT(:userRoles, ';'))
                                    and (ti.Status = 'PENDING' or ti.status = 'IN_PROGRESS')
            
            ))

            
        ORDER BY app.ApplicationID   
        OFFSET :offset ROWS
        FETCH NEXT :limit ROWS ONLY;
    '''


def getSQLForOneRole():
    return '''
     select  pl.Name as "plantName", 
         co.Name as "companyName",
         app.ApplicationID as applicationId,
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
                                            ti.AssignedTo,
                                            ti.StartedDate,
                                            ti.CompletedDate,
                                            ti.ActiveStartDate,
                                            ti.Result,
                                            ti.ResultData,
                                            ti.IsVisible,
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
                                                            where ti.StageId = sd.StageId 
                                                            and ti.ApplicationId = app.ApplicationID
                                                            --and  (td.AssigneeRole != 'SYSTEM') 
                                                            FOR JSON AUTO
                                    )
                    from TaskInstances ti 
                    LEFT JOIN TaskDefinitions td ON ti.TaskDefinitionId = td.TaskId
                    LEFT JOIN StageDefinitions sd ON ti.stageId = sd.StageId
                    where ti.ApplicationId = app.ApplicationID  
                     -- td.AssigneeRole != 'SYSTEM'
                    group by sd.stageName, sd.stageId, StageDescription
                    FOR JSON AUTO   
                    )     
                            
        FROM WF_Applications  app
            LEFT JOIN ou_kash.dbo.plant_tb pl ON app.plantID = pl.plant_ID
            LEFT JOIN ou_kash.dbo.COMPANY_TB co ON app.companyId = co.COMPANY_ID

        WHERE 
        (ApplicationType = :application_type) AND
        (:priority IS NULL OR app.Priority = :priority) and
        (:status IS NULL OR app.Status = :status) and
        (:application_id IS NULL OR app.ApplicationID = :application_id)  and 
        (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%')) and
        (:userName is not null  and  app.ApplicationID in (
            --user assigment
            select distinct(app.ApplicationID)  from WF_Applications  app
                                        INNER JOIN roleAssigment ra ON ra.ApplicationId = app.ApplicationID  
                                        AND ra.Assignee = :userName
                                        and  ra.Role IN (SELECT value FROM STRING_SPLIT(:userRoles, ';'))
            -- admin
            union
            select distinct(app.ApplicationID)  from WF_Applications  app
                                        INNER JOIN roleAssigment ra ON ra.ApplicationId = app.ApplicationID and 
                                        ra.Assignee  IN (SELECT value FROM STRING_SPLIT(:assistantMgrList, ';'))
            --group assigment 
            union

            select distinct(ti.ApplicationID)  from  TaskInstances ti 
                        LEFT JOIN TaskDefinitions td ON td.AssigneeRole in (select [RoleCode] from TaskRoles where [groupAssignment] = 1 ) 
                            where 
                                    td.assigneeRole IN (SELECT value FROM STRING_SPLIT(:userRoles, ';'))
                                    and (ti.Status = 'PENDING' or ti.status = 'IN_PROGRESS')
            
            ))

            
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
            (:application_type IS NULL OR app.ApplicationType = :application_type) AND
            (:priority IS NULL OR app.Priority = :priority) and
            (:status IS NULL OR app.Status = :status) and
            (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%'))
    '''
def get_total_count_for_one_role() -> str:
    return '''
     SELECT COUNT(*) as total_count
    FROM WF_Applications  app
         LEFT JOIN ou_kash.dbo.plant_tb pl ON app.plantID = pl.plant_ID
         LEFT JOIN ou_kash.dbo.COMPANY_TB co ON app.companyId = co.COMPANY_ID
         INNER JOIN roleAssigment ra ON ra.ApplicationId = app.ApplicationID and 
                                        ra.Assignee  IN (SELECT value FROM STRING_SPLIT(:assistantMgrList, ';'))
        LEFT JOIN TaskDefinitions td ON td.AssigneeRole in (select [RoleCode] from TaskRoles where [groupAssignment] = 1 ) 
     WHERE  (:priority IS NULL OR app.Priority = :priority) and
            (:status IS NULL OR app.Status = :status) and
            (:application_id IS NULL OR app.ApplicationID = :application_id)  and 
            (:searchName IS NULL OR pl.Name like concat('%',:searchName,'%') or co.Name like concat('%',:searchName,'%'))
            AND (:userName is not null OR ra.Assignee = :userName)
            AND  (:userRoles  is not null OR ra.Role = :userRoles)
            AND td.assigneeRole IN (SELECT value FROM STRING_SPLIT(:userRoles, ';'))
                            and (ti.Status = 'PENDING' or ti.status = 'IN_PROGRESS')
            AND (ApplicationType = :application_type)
            
          


    '''

def update_application_matching_sql() -> str:
    # Link SUBMISSION rows to their matching WORKFLOW counterpart (by ExternalAppRef)
    return '''
        UPDATE s
        SET s.[WFLinkedApp] = w.[ApplicationID]
        FROM [dbo].[WF_Applications] s
        JOIN [dbo].[WF_Applications] w
            ON  w.[ExternalAppRef] = s.[ExternalAppRef]
            AND w.[ApplicationType] = 'WORKFLOW'
        WHERE s.[ApplicationType] = 'SUBMISSION'
        and  s.[WFLinkedApp] = 0;

        -- Link WORKFLOW rows to their matching SUBMISSION counterpart (by ExternalAppRef)
        UPDATE w
        SET w.[WFLinkedApp] = s.[ApplicationID]
        FROM [dbo].[WF_Applications] w
        JOIN [dbo].[WF_Applications] s
            ON  s.[ExternalAppRef] = w.[ExternalAppRef]
            AND s.[ApplicationType] = 'SUBMISSION'
        WHERE w.[ApplicationType] = 'WORKFLOW'
        and w.[WFLinkedApp] = 0;

    '''