from datetime import datetime
from database import models
from database.models import ProcessDefinition, TaskDefinition, WFApplication, WorkflowHistory, TaskInstance, TaskFlow 
from flask import request, jsonify, session
import logging
from datetime import timezone, datetime
from logic.logic_discovery.workflow_engine import call_script_engine_post, call_task_script_engine
import safrs
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from security.system.authorization import Security


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
    
    # ==================================================
    #        WORKFLOW ENDPOINTS (Flask)
    # ==================================================
   
    @app.route('/complete_task', methods=['POST','OPTIONS'])
    @admin_required()
    @jwt_required()
    def complete_task():
        """
        This will Complete a task in the workflow and trigger the next task(s) defined in TaskFlow as needed.

        # Example PowerShell command to complete a task in the workflow
        $body = @{
            task_instance_id = 454
            result = "Approved"             --  used by Condition tasks 
            completed_by = "tband"          -- user completing the task
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
        completion_notes = data.get("completion_notes",'Complete Task via API')
        result = data.get("result", None)
        access_token = request.headers.get("Authorization")
        app_logger.debug(f'Completing task: {task_instance_id} by {completed_by} using result: {result}')
        #print(f'Completing task: {task_instance_id} by {completed_by} using result: {result}')
        if status.upper() in ['PENDING', 'IN_PROGRESS', 'IN PROGRESS']:
            task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
            if not task_instance:
                return jsonify({"status": "error", "message": "Task instance not found"}), 404
            if task_instance.Status == 'COMPLETED':
                return jsonify({"status": "error", "message": "Task is already completed"}), 400
            task_instance.Status = 'IN_PROGRESS' if status.upper() == 'IN PROGRESS' else status.upper()
            task_instance.ModifiedDate = datetime.now(timezone.utc)
            task_instance.AssignedTo = completed_by
            session.add(task_instance)
            session.commit()
            return jsonify({"status": "success", "message": f"Task status updated to {status} successfully"}), 200
        
        return _complete_task(task_instance_id=task_instance_id, result=result, completed_by=completed_by, completion_notes=completion_notes, access_token=access_token, depth=0)

    
    @app.route('/validate_tasks', methods=['GET','OPTIONS'])
    #@jwt_required()
    def validate_tasks():   
        '''
        Validate tasks in the workflow -- INTERNAL ONLY - NOT EXPOSED TO USERS
        Make sure each TaskFlow is linked From/To TaskId

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
        process_id = process_def.ProcessId
        task_defs = TaskDefinition.query.filter_by(ProcessId=process_id).all()
        if not task_defs:
            return jsonify({"status": "error", "message": f"No Task definitions found for process: {process_name}"}), 404
        task_flow_errors = []
        for task in task_defs:
            from_task = task.TaskFlowList
            to_task = task.ToTaskTaskFlowList
            category = task.TaskCategory
            task_type = task.TaskType
        
            if not from_task and task_type != 'END':
                task_flow_errors.append({"status": "error", "message": f"Task {task.TaskName} (ID: {task.TaskId}) has no incoming TaskFlow"})
            if not to_task and task_type != 'START':
                task_flow_errors.append({"status": "error", "message": f"Task {task.TaskName} (ID: {task.TaskId}) has no outgoing TaskFlow"})
            #print(f'Task {task.TaskName} (ID: {task.TaskId}) is valid with {len(from_task)} incoming and {len(to_task)} outgoing TaskFlows')
        if task_flow_errors:
            for tfe in task_flow_errors:
                app_logger.error(tfe['message'])
            return jsonify(task_flow_errors), 400
        else:
            app_logger.info(f'All TaskFlows are valid for process: {process_name}')
        return jsonify({"status": "ok", "message": "All TaskFlows are valid"}), 200

        # ==================================================
        #        END WORKFLOW ENDPOINTS (Flask)
        # ==================================================
  


def _complete_task(task_instance_id: int, result: str = None, completed_by: str = 'SYSTEM', completion_notes: str = 'Complete Task via API', access_token:str=None, depth:int=0):
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

        # Go To TaskFlow from TaskId and check to see if all the prior states are completed
        task_def = task_instance.TaskDef
        if not task_def:
            app_logger.error(f'TaskDefinition not found: {task_instance.TaskId}')
            return jsonify({"status": "error", "message": "TaskDefinition not found"}), 404

        if task_instance.Status not in ['PENDING','FAILED', 'IN_PROGRESS'] and task_def.TaskType != 'START': #and depth == 0
            app_logger.error(f'Cannot complete task {task_instance_id}-{task_instance.TaskDef.TaskName}. Task {task_instance.TaskDef.TaskType} is not PENDING or IN_PROGRESS -> {task_instance.Status}.')
            return jsonify({"status": "error", "message": f"Cannot complete task -{task_instance.TaskDef.TaskName}. Task is not PENDING or IN_PROGRESS -> {task_instance.Status}."}), 400
        
        task_name = task_def.TaskName
        
        # TIMING: Get application
        t2 = time.time()
        application_id = task_instance.Stage.ProcessInstance.ApplicationId
        application = WFApplication.query.filter_by(ApplicationID=application_id).first()
        timings['query_application'] = time.time() - t2
        
        if application and application.Status in ["WTH","COMPL"] and task_name != "Notify Customer" and task_name != 'End Certification':
            app_logger.error(f'Cannot complete task {task_instance_id}-{task_instance.TaskDef.TaskName}. Application {application.ApplicationID} status is {application.Status}.')
            return jsonify({"status": "error", "message": f"Cannot complete task -{task_instance.TaskDef.TaskName}. Application status is {application.Status}."}), 400
       
        # TIMING: Get stage list
        t3 = time.time()
        stages_list = get_stage_list(task_instance)
        timings['get_stage_list'] = time.time() - t3
        
        app_logger.info(f'[PERF] Completing TaskInstance: {task_instance_id} - {task_name} Result: {result} Depth: {depth}')
        task_flows_from = task_def.ToTaskTaskFlowList or []
        task_flows_to = task_def.TaskFlowList or []
        
        # TIMING: Check prior tasks
        t4 = time.time()
        if task_def.TaskType not in ["START", "LANEEND", "END"]:
            for tf in task_flows_from:
                prior_task_id = tf.FromTaskId
                prior_task_instance = TaskInstance.query.filter(
                    TaskInstance.TaskId == prior_task_id
                    ,TaskInstance.StageId.in_(stages_list)
                ).first()
                if prior_task_instance and prior_task_instance.Status != 'COMPLETED':
                    app_logger.error(f'Cannot complete task  {task_name} - {task_instance_id}. Prior task {prior_task_instance.TaskDef.TaskName}-{prior_task_id} status is not COMPLETED.')
                    return jsonify({"status": "error", "message": f"Cannot complete task. Prior task {prior_task_id} is not COMPLETED."}), 400
        timings['check_prior_tasks'] = time.time() - t4
        
        # Complete the task
        if depth > 0 and task_def.TaskType == 'CONDITION' and result is None:
            status = 'PENDING'
        else:
            status = "COMPLETED"
            task_instance.CompletedDate = datetime.now(timezone.utc)
            task_instance.ResultData = completion_notes
            task_instance.AssignedTo = completed_by
        
        task_instance.ModifiedDate = datetime.now(timezone.utc)
        task_instance.Status = status
        task_instance.Result = result
        session.add(task_instance)
        
        # TIMING: Commit and flush
        t5 = time.time()
        try:
            session.commit()
            session.flush()
            timings['commit_flush'] = time.time() - t5
            
            # TIMING: Call script engine
            t6 = time.time()
            if status == 'COMPLETED':
                data = None #call_task_script_engine(task_instance, access_token)
                #task_instance.ResultData = data.Message if data and 'Message' in data and data.Result else None
                if data and str(data.Result) != 'DotMap()' and  data.Result == False:
                    task_instance.ErrorMessage = data.ErrorMessage if 'ErrorMessage' in data else 'TaskInstance script returned False result'
                    task_instance.Status = 'IN_PROGRESS' if task_instance.TaskDef.TaskType != 'START' else status
                    task_instance.Result = None
                    session.add(task_instance)
                    session.commit()
                    session.flush()
                    insert_workflow_history(task_instance, status=task_instance.Status, result=result, completed_by=completed_by, completion_notes=f'TaskInstance script returned false error: {task_instance.ErrorMessage}', priorStatus='COMPLETED')  
                    app_logger.error(f'TaskInstance script returned false result for task {task_name} - {task_instance_id}')
                    return jsonify({"status": "error", "message": f'TaskInstance script returned false result for task {task_name} - {task_instance_id} message: {task_instance.ErrorMessage}'}), 400
            timings['script_engine'] = time.time() - t6
                   
        except Exception as e:
            app_logger.error(f'Error completing task {task_instance_id}: {e}')
            session.rollback()
            return jsonify({"status": "error", "message": "Error completing task"}), 500

        ## Get the workflow history
        #insert_workflow_history(task_instance, status=status, result=result, completed_by=completed_by, completion_notes=completion_notes, priorStatus='PENDING' if depth == 0 else 'COMPLETED')
        
        # TIMING: Process next tasks
        t7 = time.time()
        next_task_count = 0
        for flow_to in task_flows_to:
            next_task_id = flow_to.ToTaskId
            next_task_instance = TaskInstance.query.filter(TaskInstance.TaskId == next_task_id,
                                                            TaskInstance.StageId.in_(stages_list)).first()
            task_def = next_task_instance.TaskDef if next_task_instance else None
            condition = flow_to.Condition if task_def else None
            # If this is a condition task, check the result to see if we should proceed
            if condition and result and condition != 'None' and condition.lower() != result.lower():
                app_logger.info(f"Skipping dependency check for task {task_def.TaskName} because condition '{condition}' does not match result '{result}'.")
                continue  # Skip this dependency as the condition does not match the result
            elif next_task_instance and validate_prior_tasks(task_def, stages_list, result):
                next_task_instance.Status = 'PENDING'
                next_task_instance.AssignedTo = completed_by
                next_task_instance.StartedDate = datetime.now(timezone.utc)
                session.add(next_task_instance)    
                session.commit()
                next_task_count += 1
            if next_task_instance and next_task_instance.TaskDef.AutoComplete:  # and (validate_prior_tasks(next_task_instance.TaskDef, stages_list, result) or next_task_instance.TaskDef.TaskType in ['END', 'LANEEND']):
                # RECURSIVE CALL to complete the next task if AutoComplete is set
                _complete_task(task_instance_id=next_task_instance.TaskInstanceId, result=None, completed_by='system', completion_notes='Auto-completed', access_token=access_token, depth=depth+1)
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
                       f'StageList:{timings.get("get_stage_list",0):.3f}s, '
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

def validate_prior_tasks(taskDef: TaskDefinition, stages_list: list, result: str = None) -> bool:
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
            from_task_instance = TaskInstance.query.filter(TaskInstance.TaskId == from_task_def_id, 
                                                           TaskInstance.StageId.in_(stages_list)).first()
            if from_task_instance and from_task_instance.Status != 'COMPLETED':
                app_logger.info(f"Cannot proceed with task {taskDef.TaskName} because dependency task {from_task_instance.TaskDef.TaskName} Status is not set to: COMPLETED.")
                return False
        return True

def get_stage_list(task_instance: TaskInstance) -> list:
    '''
    Get the list of stages for a given task instance.
    '''
    stages = []
    if task_instance is None:
        return stages

    stage_instances = task_instance.Stage.ProcessInstance.StageInstanceList
    for stage_instance in stage_instances:
        stages.append(stage_instance.StageInstanceId)
    return stages

def insert_workflow_history(task_instance: TaskInstance, status: str, result: str, completed_by: str, completion_notes: str, priorStatus: str = None) -> dict:
    """
    Insert a message for a workflow application.

    Args:
        session: SQLAlchemy session
        application_id: ID of the workflow application
        process_id: ID of the process definition
        message: Message content
        created_by: User who created the message

    Returns:
        A dictionary containing the result of the operation.
    """
    task_name = task_instance.TaskDef.TaskName if task_instance and task_instance.TaskDef else 'N/A'
    application_id = task_instance.Stage.ProcessInstance.ApplicationId
    wf_history = WorkflowHistory(
            InstanceId= task_instance.Stage.ProcessInstance.InstanceId,
            TaskInstanceId=task_instance.TaskInstanceId,
            Action=f'{task_name} changed to {status} with result: {result}' if result else f'{task_name} {status}',
            NewStatus=status,
            PreviousStatus=priorStatus,
            ActionBy=completed_by,
            ActionReason=completion_notes
        )
    session.add(wf_history)
    session.commit()
    session.flush()
    app_logger.info(f'Inserted workflow message for Application ID: {application_id}')
    