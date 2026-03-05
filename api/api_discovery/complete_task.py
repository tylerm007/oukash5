from datetime import datetime
from database import models
from database.models import ProcessDefinition, TaskDefinition, WFApplication, TaskInstance, TaskFlow, TaskEvent
from flask import request, jsonify, session
import logging
from datetime import timezone, datetime
from logic.logic_discovery.workflow_engine import call_task_script_engine
import safrs
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required
from security.system.authorization import Security
from database.cache_service import DatabaseCacheService
import threading
import uuid
import json

cache = DatabaseCacheService.get_instance()

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None
_flask_app = None  # Store Flask app for background tasks

# Background task tracking for long-running script executions
background_script_tasks = {}

class BackgroundTaskStatus:
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir, _flask_app
    _project_dir = project_dir
    _flask_app = app  # Store Flask app reference for background tasks
    pass

    # ==================================================
    #        WORKFLOW ENDPOINTS (Flask)
    # ==================================================
   
    @app.route('/complete_task', methods=['POST','OPTIONS'])
    @jwt_required()
    def complete_task():
        """
        This will Complete a task in the workflow and trigger the next task(s) defined in TaskFlow as needed.

        # Example PowerShell command to complete a task in the workflow
        $body = @{
            task_instance_id = 454
            result = "Approved"             --  used by Condition tasks 
            completed_by = "tband"          -- user completing the task
            capacity = "ADMIN"              -- ADMIN, MEMBER, DESIGNATED
            completion_notes = "Task completed successfully" -- writes to WFHistory
        } | ConvertTo-Json)

        Invoke-RestMethod -Uri "http://localhost:5656/complete_task" -Method POST -Body $body -ContentType "application/json"
    
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200       
        
        data = request.get_json()
        task_instance_id = data.get("task_instance_id")
        status = data.get("status", 'COMPLETED')
        if not task_instance_id:
            return jsonify({"status": "error", "message": "task_instance_id is required"}), 400
        user = Security.current_user().Username
        completed_by = data.get("completed_by",user)
        capactity = data.get("capacity", None) # "S/B ADMIN, MEMBER, DESIGNATED"
        completion_notes = data.get("completion_notes",'Complete Task via API')
        result = data.get("result", None)
        access_token = request.headers.get("Authorization")
        app_logger.debug(f'Completing task: {task_instance_id} by {completed_by} using result: {result}')
        #print(f'Completing task: {task_instance_id} by {completed_by} using result: {result}')
        if status.upper() in ['PENDING', 'IN_PROGRESS', 'IN PROGRESS']:
            task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
            if not task_instance:
                return jsonify({"status": "error", "message": "Task instance not found"}), 404
            task_def = task_instance.TaskDefinition
            if task_instance.Status == 'COMPLETED' and task_def.TaskName != 'Legal Review':  # Allow re-completing Legal Review tasks to handle restarts
                return jsonify({"status": "error", "message": "Task is already completed"}), 400
            priorStatus = task_instance.Status
            task_instance.Status = 'IN_PROGRESS' if status.upper() == 'IN PROGRESS' else status.upper()
            task_instance.ModifiedDate = datetime.now()
            #task_instance.CompletedBy = completed_by
            session.add(task_instance)
            session.commit()
            insert_workflow_history(task_instance, status=task_instance.Status, result=result, completed_by=completed_by, completion_notes=f'TaskInstance {task_instance.TaskInstanceId} updated', priorStatus=priorStatus, details=task_instance.ResultData)  
                    
            return jsonify({"status": "success", "message": f"Task {task_instance_id} status updated to {status} successfully"}), 200
        
        return _complete_task(task_instance_id=task_instance_id, result=result, completed_by=completed_by, completion_notes=completion_notes, access_token=access_token, capacity=capactity, depth=0)

    
    @app.route('/validate_tasks', methods=['GET','OPTIONS'])
    #@jwt_required()
    def validate_tasks():   
        '''
        Validate tasks in the workflow -- INTERNAL ONLY - NOT EXPOSED TO USERS
        Make sure each TaskFlow is linked From/To TaskDefinitionId

        curl -X GET http://localhost:5656/validate_tasks?process_name="OU Certification Workflow" \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer <your_jwt_token>"

        Invoke-RestMethod -Uri "http://localhost:5656/validate_tasks" -Method GET -ContentType "application/json"
            -Headers @{Authorization = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1OTkyODE2MCwianRpIjoiZWYyOTdiYTQtMTlkYS00NDdiLWEzNmMtNzhmMTMzNDg0NjUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzU5OTI4MTYwLCJleHAiOjE3NTk5NDE0ODB9.kwcOIfJpWsF-UBfW087pk_9YZ4pRO9iegnEmhGSdEoM"}
        Returns:
            json: response        
        '''
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200 
        access_token = request.headers.get("Authorization")
        #data = request.args if request.args else {}
        process_name = request.args.get('process_name',"OU Application Init")
        if not process_name:
            return jsonify({"status": "error", "message": "process_name is required"}), 400
        process_def = ProcessDefinition.query.filter_by(ProcessName=process_name, IsActive=True).first()
        if not process_def:
            return jsonify({"status": "error", "message": f"Process definition not found: {process_name}"}), 404
        process__def_id = process_def.ProcessId
        task_defs = TaskDefinition.query.filter_by(ProcessDefinitionId=process__def_id).all()
        if not task_defs:
            return jsonify({"status": "error", "message": f"No Task definitions found for process: {process_name}"}), 404
        task_flow_errors = []
        for task in task_defs:
            from_task = task.TaskFlowList
            to_task = task.ToTaskTaskFlowList
            category = task.TaskCategory
            task_type = task.TaskType
        
            if not from_task and task_type != 'END':
                task_flow_errors.append({"status": "error", "message": f"Task {task.TaskName} - {task_type} (ID: {task.TaskId}) has no incoming TaskFlow"})
            if not to_task and task_type != 'START':
                task_flow_errors.append({"status": "error", "message": f"Task {task.TaskName} - {task_type} (ID: {task.TaskId}) has no outgoing TaskFlow"})
            #print(f'Task {task.TaskName} (ID: {task.TaskDefinitionId}) is valid with {len(from_task)} incoming and {len(to_task)} outgoing TaskFlows')
        if task_flow_errors:
            for tfe in task_flow_errors:
                app_logger.error(tfe['message'])
            return jsonify(task_flow_errors), 400
        else:
            app_logger.info(f'All TaskFlows are valid for process: {process_name}')
        return jsonify({"status": "ok", "message": "All TaskFlows are valid"}), 200

    @app.route('/complete_task_async', methods=['POST','OPTIONS'])
    @jwt_required()
    def complete_task_async():
        """
        Complete a task in the background for long-running script executions.
        Returns immediately with a task_id to check status later.

        Example PowerShell command:
        $body = @{
            task_instance_id = 454
            result = "Approved"
            completed_by = "tband"
            capacity = "ADMIN"
            completion_notes = "Task completed successfully"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "http://localhost:5656/complete_task_async" -Method POST -Body $body -ContentType "application/json"
        
        Returns:
            202 Accepted with task_id to check status at /task_script_status/{task_id}
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.get_json()
        task_instance_id = data.get("task_instance_id")
        
        if not task_instance_id:
            return jsonify({"status": "error", "message": "task_instance_id is required"}), 400
        status = data.get("status", 'COMPLETED')
        if not status:
            return jsonify({"status": "error", "message": "status is required"}), 400
        user = Security.current_user().Username
        
        completed_by = data.get("completed_by", user)
        capacity = data.get("capacity", None)
        completion_notes = data.get("completion_notes", 'Complete Task via API (Async)')
        result = data.get("result", None)
        access_token = request.headers.get("Authorization")
        
        task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
        if not task_instance:
            return jsonify({"status": "error", "message": f"Task instance {task_instance_id} not found"}), 404
        if task_instance.Status == 'COMPLETED':
            return jsonify({"status": "error", "message": f"Task instance {task_instance_id} is already completed"}), 400
        if status.upper() in ['PENDING', 'IN_PROGRESS', 'IN PROGRESS']:
            task_instance.Status = 'IN_PROGRESS' if status.upper() == 'IN PROGRESS' else status.upper()
            task_instance.ModifiedDate = datetime.now()
            #task_instance.CompletedBy = completed_by
            session.add(task_instance)
            session.commit()
            return jsonify({"status": "success", "message": f"Task {task_instance_id} status updated to {status} successfully"}), 200
        
        # Generate unique background task ID
        bg_task_id = str(uuid.uuid4())
        
        # Initialize background task status
        background_script_tasks[bg_task_id] = {
            'status': BackgroundTaskStatus.PENDING,
            'created_at': datetime.now(),
            'task_instance_id': task_instance_id,
            'completed_by': completed_by,
            'result': None,
            'error': None
        }
        
        # Start background thread
        thread = threading.Thread(
            target=_complete_task_background,
            args=(bg_task_id, task_instance_id, result, completed_by, completion_notes, access_token, capacity)
        )
        thread.daemon = True
        thread.start()
        
        app_logger.info(f'Started background task completion: {bg_task_id} for TaskInstance: {task_instance_id}')
        return jsonify({
            "status": "accepted",
            "task_id": bg_task_id,
            "task_instance_id": task_instance_id,
            "message": "Task completion started in background",
            "check_status_url": f"/task_script_status/{bg_task_id}"
        }), 202

    @app.route('/task_script_status/<task_id>', methods=['GET'])
    @jwt_required()
    def get_task_script_status(task_id):
        """
        Check the status of a background task script execution.
        
        Usage: GET /task_script_status/{task_id}
        
        Returns:
            JSON with status: pending, running, completed, or failed
        """
        if task_id not in background_script_tasks:
            return jsonify({"status": "error", "message": "Task not found"}), 404
        
        task = background_script_tasks[task_id]
        response = {
            "task_id": task_id,
            "status": task['status'],
            "created_at": task['created_at'].isoformat(),
            "task_instance_id": task['task_instance_id'],
            "completed_by": task['completed_by']
        }
        
        if 'started_at' in task:
            response['started_at'] = task['started_at'].isoformat()
        
        if task['status'] == BackgroundTaskStatus.COMPLETED:
            response['result'] = task['result']
            if 'completed_at' in task:
                response['completed_at'] = task['completed_at'].isoformat()
                response['duration_seconds'] = (task['completed_at'] - task['created_at']).total_seconds()
        elif task['status'] == BackgroundTaskStatus.FAILED:
            response['error'] = task['error']
            if 'failed_at' in task:
                response['failed_at'] = task['failed_at'].isoformat()
        
        return jsonify(response)

        # ==================================================
        #        END WORKFLOW ENDPOINTS (Flask)
        # ==================================================
  


def _complete_task(task_instance_id: int, result: str = None, completed_by: str = 'SYSTEM', completion_notes: str = 'Complete Task via API', access_token:str=None, capacity:str =  None, depth:int=0):
        '''Complete a task instance in the workflow and trigger the next task(s) as needed.'''
        
        # START PERFORMANCE TIMING
        import time
        start_time = time.time()
        timings = {}
        
        # TIMING: Query task instance
        t1 = time.time()
        task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
        timings['query_task_instance'] = time.time() - t1
        
        if not task_instance:
            app_logger.error(f'TaskInstance not found: {task_instance_id}')
            return jsonify({"status": "error", "message": "TaskInstance not found"}), 404

        # Go To TaskFlow from TaskDefinitionId and check to see if all the prior states are completed
        task_def = task_instance.TaskDefinition
        if not task_def:
            app_logger.error(f'TaskDefinition not found: {task_instance.TaskDefinitionId}')
            return jsonify({"status": "error", "message": "TaskDefinition not found"}), 404

        if task_instance.Status not in ['PENDING','FAILED', 'IN_PROGRESS'] and task_def.TaskType != 'START': #and depth == 0
            app_logger.error(f'Cannot complete task {task_instance_id}-{task_def.TaskName}. Task {task_def.TaskType} is not PENDING or IN_PROGRESS -> {task_instance.Status}.')
            return jsonify({"status": "error", "message": f"Cannot complete task -{task_def.TaskName}. Task is not PENDING or IN_PROGRESS -> {task_instance.Status}."}), 400
        
        task_name = task_def.TaskName
        
        # TIMING: Get application
        t2 = time.time()
        application_id = task_instance.ApplicationId
        application = WFApplication.query.filter_by(ApplicationID=application_id).first()
        timings['query_application'] = time.time() - t2
        
        if application and application.Status in ["WTH","COMPL"] and task_name != "Notify Customer" and task_name != 'End Certification':
            app_logger.error(f'Cannot complete task {task_instance_id}-{task_instance.TaskDefinition.TaskName}. Application {application.ApplicationID} status is {application.Status}.')
            return jsonify({"status": "error", "message": f"Cannot complete task -{task_instance.TaskDefinition.TaskName}. Application status is {application.Status}."}), 400
       
        # TIMING: Get stage list
        t3 = time.time()
        #stages_list = get_stage_list(task_instance)
        #stages_list = [StageId for StageId in cache.get_all_stage_definitions()]
        timings['get_stage_list'] = time.time() - t3
        
        app_logger.info(f'[PERF] Completing TaskInstance: {task_instance_id} - {task_name} Result: {result} Depth: {depth}')
        task_flows_from = task_def.ToTaskTaskFlowList or []
        task_flows_to = task_def.TaskFlowList or []
        
        # TIMING: Check prior tasks
        t4 = time.time()
        if task_def.TaskType not in ["START", "STAGEEND", "END"]:
            for tf in task_flows_from:
                prior_task_id = tf.FromTaskId
                prior_task_instance = TaskInstance.query.filter(
                    TaskInstance.TaskDefinitionId == prior_task_id
                    ,TaskInstance.ApplicationId == task_instance.ApplicationId
                ).first()
                if prior_task_instance and prior_task_instance.Status != 'COMPLETED':
                    app_logger.error(f'Cannot complete task  {task_name} - {task_instance_id}. Prior task {prior_task_instance.TaskDefinition.TaskName}-{prior_task_id} status is not COMPLETED.')
                    return jsonify({"status": "error", "message": f"Cannot complete task {task_name} . Prior task {prior_task_id} {prior_task_instance.TaskDefinition.TaskName} is not COMPLETED."}), 400
        timings['check_prior_tasks'] = time.time() - t4
        
        # Complete the task
        result_data = task_instance.ResultData
        result_data = json.loads(result_data.replace("'", '"',1000)) if isinstance(result_data, str) and result_data.startswith('{') else {}   
        if depth > 0 and task_def.TaskType == 'CONDITION' and result is None and task_instance.IsVisible == 1:
            status = 'PENDING'
            task_instance.TaskRole = task_def['AssigneeRole']
        else:
            result_data['notes'] = completion_notes
            status = "COMPLETED"
            task_instance.CompletedDate = datetime.now()
            task_instance.ResultData = json.dumps(result_data)
            task_instance.CompletedBy = completed_by
            task_instance.CompletedCapacity = capacity
        task_instance.ErrorMessage = None
        task_instance.ModifiedDate = datetime.now()
        task_instance.Status = status
        task_instance.Result = result
        session.add(task_instance)
        session.flush()

        # TIMING: Commit and flush
        t5 = time.time()
        try:
            session.commit()
            session.flush()
            timings['commit_flush'] = time.time() - t5
            
            # TIMING: Call script engine
            t6 = time.time()
            if status == 'COMPLETED' and task_def.PostScriptJson is not None and task_def.PostScriptJson != '':
                data = None # call_task_script_engine(task_instance, access_token)
                #task_instance.ResultData = data.Message if data and 'Message' in data and data.Result else None
                if data and str(data.get("Result")) != 'DotMap()' and  data.get("Result") == False:
                    task_instance.ErrorMessage = data.get('ErrorMessage')  if 'ErrorMessage' in data else 'TaskInstance script returned False result'
                    task_instance.Status = 'IN_PROGRESS' if task_instance.TaskDefinition.TaskType != 'START' else status
                    task_instance.Result = None
                    session.add(task_instance)
                    session.commit()
                    session.flush()
                    insert_workflow_history(task_instance, status=task_instance.Status, result=result, completed_by=completed_by, completion_notes=f'TaskInstance script returned false error: {task_instance.ErrorMessage}', priorStatus='COMPLETED', details=task_instance.ErrorMessage)  
                    app_logger.error(f'TaskInstance script returned false result for task {task_name} - {task_instance_id}')
                    return jsonify({"status": "error", "message": f'TaskInstance script returned false result for task {task_name} - {task_instance_id} message: {task_instance.ErrorMessage}'}), 400
                else:
                    message = data.get('Message') if data and 'Message' in data and data.get("Result") else None
                    if message:
                        result_data['message'] = message
                        task_instance.ResultData = json.dumps(result_data)
                    session.add(task_instance)
            timings['script_engine'] = time.time() - t6
            
                   
        except Exception as e:
            app_logger.error(f'Error completing task {task_instance_id}: {e}')
            session.rollback()
            return jsonify({"status": "error", "message": "Error completing task"}), 500
        ## Get the workflow history
        insert_workflow_history(task_instance, status=status, result=result, completed_by=completed_by, completion_notes=completion_notes, priorStatus='PENDING' if depth == 0 else 'COMPLETED', details=task_instance.ResultData)
        
        # TIMING: Process next tasks
        t7 = time.time()
        next_task_count = 0
        for flow_to in task_flows_to:
            next_task_id = flow_to.ToTaskId
            next_task_instance = TaskInstance.query.filter(TaskInstance.TaskDefinitionId == next_task_id,
                                                            TaskInstance.ApplicationId == application_id).first()
            task_def = next_task_instance.TaskDefinition if next_task_instance else None
            condition = flow_to.Condition if task_def else None
            # If this is a condition task, check the result to see if we should proceed
            if condition and result and condition != 'None' and condition.lower() != result.lower():
                app_logger.info(f"Skipping dependency check for task {task_def.TaskName} because condition '{condition}' does not match result '{result}'.")
                continue  # Skip this dependency as the condition does not match the result
            elif next_task_instance and validate_prior_tasks(task_def, application_id, result):
                next_task_instance.Status = 'PENDING'
                next_task_instance.TaskRole = task_def.AssigneeRole
                next_task_instance.StartedDate = datetime.now()
                session.add(next_task_instance)    
                session.commit()
                next_task_count += 1
            if next_task_instance and next_task_instance.TaskDefinition.AutoComplete:  # and (validate_prior_tasks(next_task_instance.TaskDef, stages_list, result) or next_task_instance.TaskDef.TaskType in ['END', 'LANEEND']):
                # RECURSIVE CALL to complete the next task if AutoComplete is set
                _complete_task(task_instance_id=next_task_instance.TaskInstanceId, result=None, completed_by='SYSTEM', completion_notes='Auto-completed', access_token=access_token, depth=depth+1)
        timings['process_next_tasks'] = time.time() - t7

        # TIMING: Calculate total and log
        total_time = time.time() - start_time
        timings['recursive_time'] = timings.get('process_next_tasks', 0)
        own_time = total_time - timings['recursive_time']
        
        if depth == 0:
            app_logger.info(f'[PERF] ====== ROOT TASK {task_instance_id} ({task_name}) COMPLETED ======')
            app_logger.info(f'[PERF] TOTAL TIME: {total_time:.3f}s')
        else:
            app_logger.info(f'[PERF] Task {task_instance_id} ({task_name}) depth={depth} completed in {total_time:.3f}s')
        
        app_logger.info(f'[PERF] Breakdown (own: {own_time:.3f}s) - '
                       f'QueryTask:{timings.get("query_task_instance",0):.3f}s, '
                       f'QueryApp:{timings.get("query_application",0):.3f}s, '
                       f'CheckPrior:{timings.get("check_prior_tasks",0):.3f}s, '
                       f'Commit:{timings.get("commit_flush",0):.3f}s, '
                       f'Script:{timings.get("script_engine",0):.3f}s, '
                       f'NextTasks({next_task_count}):{timings.get("process_next_tasks",0):.3f}s')
                
        app_logger.info(f'Task completed:{task_name} - {task_instance_id} Status: {task_instance.Status} Result: {task_instance.Result}')
        
        return jsonify({
            "status": "ok", 
            "data": {
                "task_instance_id": task_instance_id,
                "processing_time": f"{total_time:.3f}s",
                "own_time": f"{own_time:.3f}s",
                "depth": depth,
                "timings": {k: f"{v:.3f}s" for k, v in timings.items()}
            }
        }), 200

def validate_prior_tasks(taskDef: TaskDefinition, application_id: int, result: str = None) -> bool:
        '''
        Validate that all prior tasks in the workflow (TaskFlow)are completed before allowing this task to proceed.
        '''
        if taskDef is None:
            return True
        dependencies = taskDef.ToTaskTaskFlowList  # List of TaskFlow objects where this task is the ToTask
        if dependencies is None or len(dependencies) == 0:
            return True  # No dependencies, so it's valid to proceed
        for dependency in dependencies:
            from_task_def_id = dependency.FromTaskId
            #condition = dependency.Condition
            #if taskDef.TaskType == 'CONDITION' and condition and result and condition != 'None' and condition.lower() == result.lower():
            #    app_logger.info(f"Skipping dependency check for task {taskDef.TaskName} because condition '{condition}' does matches result '{result}'.")
            #    continue  # Skip this dependency as the condition does not match the result
            from_task_instance = TaskInstance.query.filter(TaskInstance.TaskDefinitionId == from_task_def_id, 
                                                           TaskInstance.ApplicationId == application_id).first()
            if from_task_instance and from_task_instance.Status != 'COMPLETED':
                app_logger.info(f"Cannot proceed with task {taskDef.TaskName} because dependency task {from_task_instance.TaskDefinition.TaskName} Status is not set to: COMPLETED.")
                return False
        return True


def insert_workflow_history(task_instance: TaskInstance, status: str, result: str, completed_by: str, completion_notes: str, priorStatus: str = None, details: str = None) -> dict:
    '''
    Insert a message for a workflow application.

    Args:
        session: SQLAlchemy session
        application_id: ID of the workflow application
        process_id: ID of the process definition
        message: Message content
        created_by: User who created the message

    Returns:
        A dictionary containing the result of the operation.
    '''
    task_name = task_instance.TaskDefinition.TaskName if task_instance and task_instance.TaskDefinition else 'N/A'
    application_id = task_instance.ApplicationId if task_instance else None
    wf_history = TaskEvent(
            TaskInstanceId=task_instance.TaskInstanceId,
            ApplicationId=application_id,
            Action=f'{task_name} changed to {status} with result: {result}' if result else f'{task_name} {status}',
            NewStatus=status,
            PreviousStatus=priorStatus,
            ActionBy=completed_by,
            ActionReason=completion_notes,
            Details=details
        )
    session.add(wf_history)
    session.commit()
    session.flush()
    
    
    app_logger.info(f'Inserted workflow message for Application ID: {application_id}')


# ============================================
# BACKGROUND TASK EXECUTION
# ============================================

def _complete_task_background(bg_task_id: str, task_instance_id: int, result: str, completed_by: str, 
                              completion_notes: str, access_token: str, capacity: str):
    """
    Execute task completion in background thread.
    This allows long-running script executions to not block the API response.
    
    Args:
        bg_task_id: Unique ID for tracking this background task
        task_instance_id: The TaskInstance to complete
        result: Task result value
        completed_by: User completing the task
        completion_notes: Notes about completion
        access_token: Authorization token for API calls
        capacity: User's capacity (ADMIN, MEMBER, DESIGNATED)
    """
    # CRITICAL: Push Flask application context for database access
    if not _flask_app:
        app_logger.error(f'[BACKGROUND] Flask app not available for background task {bg_task_id}')
        background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.FAILED
        background_script_tasks[bg_task_id]['error'] = 'Flask app context not available'
        return
    
    with _flask_app.app_context():
        try:
            # Update status to running
            background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.RUNNING
            background_script_tasks[bg_task_id]['started_at'] = datetime.now()
            
            app_logger.info(f'[BACKGROUND] Starting task completion: {task_instance_id} (bg_task: {bg_task_id})')
            
            # Execute the actual task completion
            response = _complete_task(
                task_instance_id=task_instance_id,
                result=result,
                completed_by=completed_by,
                completion_notes=completion_notes,
                access_token=access_token,
                capacity=capacity,
                depth=0
            )
            
            # Check if response is a tuple (response, status_code)
            if isinstance(response, tuple):
                response_data, status_code = response
                response_json = response_data.get_json() if hasattr(response_data, 'get_json') else response_data
            else:
                response_json = response.get_json() if hasattr(response, 'get_json') else response
                status_code = 200
            
            # Update task status based on result
            if status_code >= 200 and status_code < 300:
                background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.COMPLETED
                background_script_tasks[bg_task_id]['result'] = response_json
                background_script_tasks[bg_task_id]['completed_at'] = datetime.now()
                app_logger.info(f'[BACKGROUND] Task completion succeeded: {task_instance_id} (bg_task: {bg_task_id})')
            else:
                background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.FAILED
                background_script_tasks[bg_task_id]['error'] = response_json.get('message', 'Unknown error')
                background_script_tasks[bg_task_id]['failed_at'] = datetime.now()
                app_logger.error(f'[BACKGROUND] Task completion failed: {task_instance_id} (bg_task: {bg_task_id})')
                
        except Exception as e:
            app_logger.error(f'[BACKGROUND] Critical error in task completion: {task_instance_id} (bg_task: {bg_task_id}): {e}')
            background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.FAILED
            background_script_tasks[bg_task_id]['error'] = f'Critical error: {str(e)}'
            background_script_tasks[bg_task_id]['failed_at'] = datetime.now()
    

def call_task_script_engine_async(task_instance_id: int, access_token: str) -> str:
    """
    Wrapper to call task script engine in background and return a task_id for status checking.
    
    Args:
        task_instance_id: The TaskInstance ID
        access_token: Authorization token
        
    Returns:
        task_id: UUID string to check background task status
    """
    # Validate that task instance exists (in current context)
    task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
    if not task_instance:
        raise ValueError(f"TaskInstance {task_instance_id} not found")
    
    # Generate unique background task ID
    bg_task_id = str(uuid.uuid4())
    
    # Initialize background task status
    background_script_tasks[bg_task_id] = {
        'status': BackgroundTaskStatus.PENDING,
        'created_at': datetime.now(),
        'task_instance_id': task_instance_id,
        'result': None,
        'error': None
    }
    
    # Start background thread - pass task_instance_id instead of object
    thread = threading.Thread(
        target=_execute_script_background,
        args=(bg_task_id, task_instance_id, access_token)  # Pass ID, not object
    )
    thread.daemon = True
    thread.start()
    
    app_logger.info(f'Started background script execution: {bg_task_id} for TaskInstance: {task_instance_id}')
    return bg_task_id


def _execute_script_background(bg_task_id: str, task_instance_id: int, access_token: str):
    """
    Execute task script engine in background thread.
    
    Args:
        bg_task_id: Unique ID for tracking this background task
        task_instance_id: The TaskInstance ID (will be queried within app context)
        access_token: Authorization token for API calls
    """
    # CRITICAL: Push Flask application context for database access
    if not _flask_app:
        app_logger.error(f'[BACKGROUND] Flask app not available for background task {bg_task_id}')
        background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.FAILED
        background_script_tasks[bg_task_id]['error'] = 'Flask app context not available'
        return
    
    with _flask_app.app_context():
        try:
            # Query task instance within app context
            task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
            if not task_instance:
                raise ValueError(f"TaskInstance {task_instance_id} not found")
            
            # Update status to running
            background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.RUNNING
            background_script_tasks[bg_task_id]['started_at'] = datetime.now()
            
            app_logger.info(f'[BACKGROUND] Starting script execution for TaskInstance: {task_instance_id} (bg_task: {bg_task_id})')
            
            # Execute the script
            result = call_task_script_engine(task_instance, access_token)
            
            # Update task status
            background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.COMPLETED
            background_script_tasks[bg_task_id]['result'] = result
            background_script_tasks[bg_task_id]['completed_at'] = datetime.now()
            
            app_logger.info(f'[BACKGROUND] Script execution completed for TaskInstance: {task_instance_id} (bg_task: {bg_task_id})')
            
        except Exception as e:
            app_logger.error(f'[BACKGROUND] Script execution failed for TaskInstance: {task_instance_id} (bg_task: {bg_task_id}): {e}')
            background_script_tasks[bg_task_id]['status'] = BackgroundTaskStatus.FAILED
            background_script_tasks[bg_task_id]['error'] = str(e)
            background_script_tasks[bg_task_id]['failed_at'] = datetime.now()
    
