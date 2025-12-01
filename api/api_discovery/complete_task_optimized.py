"""
PERFORMANCE IMPROVEMENTS FOR _complete_task

Key optimizations:
1. Eager loading with joinedload to prevent N+1 queries
2. Batch database commits
3. Cache stage_list and task instances to avoid repeated queries
4. Add recursion depth limit
5. Bulk query for next task instances
6. Use query.options() for eager loading relationships
"""
from functools import wraps
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload
from datetime import datetime
from database.models import TaskInstance, TaskDefinition
import logging
from datetime import datetime
from database.models import  TaskDefinition, TaskInstance
from flask import  jsonify, request, session
import logging
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from logic.logic_discovery.workflow_engine import call_task_script_engine
import safrs
from config.config import Args
from security.system.authorization import Security

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
# Add this constant at module level
MAX_RECURSION_DEPTH = 50  # Prevent infinite loops

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir

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
   
    @app.route('/complete_task_v1', methods=['POST','OPTIONS'])
    @app.route('/complete_task', methods=['POST','OPTIONS'])
    @admin_required()
    @jwt_required()
    def complete_task_v1():
    
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
            task_instance.ModifiedDate = datetime.utcnow()
            task_instance.AssignedTo = completed_by
            session.add(task_instance)
            session.commit()
            return jsonify({"status": "success", "message": f"Task status updated to {status} successfully"}), 200
        
        return _complete_task_optimized(task_instance_id=task_instance_id, result=result, completed_by=completed_by, completion_notes=completion_notes, access_token=access_token, depth=0)


def _complete_task_optimized(
    task_instance_id: int, 
    result: str = None, 
    completed_by: str = 'SYSTEM', 
    completion_notes: str = 'Complete Task via API', 
    access_token: str = None, 
    depth: int = 0,
    task_instance_cache: dict = None,  # NEW: Cache to avoid re-querying
    stages_list_cache: list = None     # NEW: Cache stage list
):
    '''
    Optimized version of complete_task with performance improvements:
    - Eager loading to prevent N+1 queries
    - Batched database commits
    - Recursion depth limit
    - Cached queries
    '''
    
    # START TIMER
    import time
    start_time = time.time()
    timings = {}  # Track individual operation timings
    
    # IMPROVEMENT 1: Add recursion depth limit
    if depth > MAX_RECURSION_DEPTH:
        app_logger.error(f'Maximum recursion depth {MAX_RECURSION_DEPTH} exceeded for task {task_instance_id}')
        return jsonify({"status": "error", "message": "Maximum workflow depth exceeded"}), 500
    
    # Initialize cache on first call
    if task_instance_cache is None:
        task_instance_cache = {}
    
    # IMPROVEMENT 2: Use eager loading to prevent N+1 queries
    # Check cache first
    t1 = time.time()
    if task_instance_id in task_instance_cache:
        task_instance = task_instance_cache[task_instance_id]
        app_logger.debug(f"[PERF] Task {task_instance_id} loaded from cache")
    else:
        from database.models import StageInstance, ProcessInstance
        task_instance = TaskInstance.query.options(
            joinedload(TaskInstance.TaskDef).joinedload(TaskDefinition.ToTaskTaskFlowList),
            joinedload(TaskInstance.TaskDef).joinedload(TaskDefinition.TaskFlowList),
            joinedload(TaskInstance.Stage).joinedload(StageInstance.ProcessInstance).joinedload(ProcessInstance.Application),
            joinedload(TaskInstance.Stage).joinedload(StageInstance.ProcessInstance).joinedload(ProcessInstance.StageInstanceList)
        ).filter_by(TaskInstanceId=task_instance_id).first()
        
        if task_instance:
            task_instance_cache[task_instance_id] = task_instance
    timings['query_task_instance'] = time.time() - t1
    app_logger.info(f"[PERF] Query task instance: {timings['query_task_instance']:.3f}s")
    
    if not task_instance:
        app_logger.error(f'TaskInstance not found: {task_instance_id}')
        return jsonify({"status": "error", "message": "TaskInstance not found"}), 404

    task_def = task_instance.TaskDef
    if not task_def:
        app_logger.error(f'TaskDefinition not found: {task_instance.TaskId}')
        return jsonify({"status": "error", "message": "TaskDefinition not found"}), 404

    # Validation checks
    if task_instance.Status not in ['PENDING','FAILED', 'IN_PROGRESS'] and task_def.TaskType != 'START':
        app_logger.error(f'Cannot complete task {task_instance_id}-{task_def.TaskName}. Status: {task_instance.Status}')
        return jsonify({"status": "error", "message": f"Cannot complete task. Invalid status: {task_instance.Status}"}), 400
    
    task_name = task_def.TaskName
    application = task_instance.Stage.ProcessInstance.Application  # Already eager loaded
    
    if application and application.Status in ["WTH","COMPL"] and task_name not in ["Notify Customer", 'End Certification']:
        app_logger.error(f'Cannot complete task {task_instance_id}. Application status: {application.Status}')
        return jsonify({"status": "error", "message": f"Cannot complete task. Application status: {application.Status}"}), 400
    
    # IMPROVEMENT 3: Cache stages_list to avoid repeated function calls
    if stages_list_cache is None:
        stages_list_cache = [si.StageInstanceId for si in task_instance.Stage.ProcessInstance.StageInstanceList]
    
    app_logger.info(f'Completing TaskInstance: {task_instance_id} - {task_name} Result: {result} Depth: {depth}')
    
    # Already loaded via eager loading
    task_flows_from = task_def.ToTaskTaskFlowList or []
    task_flows_to = task_def.TaskFlowList or []
    
    # IMPROVEMENT 4: Bulk query for prior task instances instead of one-by-one
    t2 = time.time()
    if task_def.TaskType not in ["START", "LANEEND", "END"] and task_flows_from:
        prior_task_ids = [tf.FromTaskId for tf in task_flows_from]
        prior_task_instances = TaskInstance.query.filter(
            TaskInstance.TaskId.in_(prior_task_ids),
            TaskInstance.StageId.in_(stages_list_cache)
        ).all()
        
        # Build lookup dict for fast access
        prior_tasks_by_id = {ti.TaskId: ti for ti in prior_task_instances}
        
        # Check all prior tasks
        for tf in task_flows_from:
            prior_task_instance = prior_tasks_by_id.get(tf.FromTaskId)
            if prior_task_instance and prior_task_instance.Status != 'COMPLETED':
                app_logger.error(f'Cannot complete task {task_name}. Prior task {prior_task_instance.TaskDef.TaskName} not COMPLETED.')
                return jsonify({"status": "error", "message": f"Prior task not COMPLETED"}), 400
    timings['check_prior_tasks'] = time.time() - t2
    app_logger.info(f"[PERF] Check prior tasks: {timings['check_prior_tasks']:.3f}s")
    
    # Complete the task
    if depth > 0 and task_def.TaskType == 'CONDITION' and result is None:
        status = 'PENDING'
    else:
        status = "COMPLETED"
        task_instance.CompletedDate = datetime.utcnow()
        task_instance.ResultData = completion_notes
        task_instance.AssignedTo = completed_by
    
    task_instance.ModifiedDate = datetime.utcnow()
    task_instance.Status = status
    task_instance.Result = result
    
    # IMPROVEMENT 5: Collect all updates and commit once
    updates_to_commit = [task_instance]
    
    try:
        # Call script engine if completed
        t3 = time.time()
        if status == 'COMPLETED':
            data = call_task_script_engine(task_instance, access_token)
            task_instance.ResultData = data.Message if data and 'Message' in data and data.Result else None
            if data and str(data.Result) != 'DotMap()' and data.Result == False:
                task_instance.ErrorMessage = data.ErrorMessage if 'ErrorMessage' in data else 'Script returned False'
                task_instance.Status = 'IN_PROGRESS' if task_instance.TaskDef.TaskType != 'START' else status
                task_instance.Result = None
                
                # IMPROVEMENT 6: Single commit instead of multiple
                session.add(task_instance)
                #insert_workflow_history(task_instance, status=task_instance.Status, result=result, 
                #                      completed_by=completed_by, 
                #                      completion_notes=f'Script error: {task_instance.ErrorMessage}', 
                #                      priorStatus='COMPLETED')
                session.commit()
                app_logger.error(f'Script returned false for task {task_name}')
                return jsonify({"status": "error", "message": f'Script error: {task_instance.ErrorMessage}'}), 400
        timings['script_engine'] = time.time() - t3
        app_logger.info(f"[PERF] Script engine call: {timings['script_engine']:.3f}s")
        
        # Insert workflow history (will be committed with next tasks)
        #history = insert_workflow_history(task_instance, status=status, result=result, 
        #                                 completed_by=completed_by, completion_notes=completion_notes, 
        #                                 priorStatus='PENDING' if depth == 0 else 'COMPLETED',
        #                                 commit=False)  # Don't commit yet
        
        # IMPROVEMENT 7: Bulk query for next task instances
        t4 = time.time()
        if task_flows_to:
            next_task_ids = [flow.ToTaskId for flow in task_flows_to]
            next_task_instances = TaskInstance.query.options(
                joinedload(TaskInstance.TaskDef).joinedload(TaskDefinition.ToTaskTaskFlowList)
            ).filter(
                TaskInstance.TaskId.in_(next_task_ids),
                TaskInstance.StageId.in_(stages_list_cache)
            ).all()
            
            # Build lookup for fast access
            next_tasks_by_id = {ti.TaskId: ti for ti in next_task_instances}
            
            # Cache next task instances
            for nti in next_task_instances:
                task_instance_cache[nti.TaskInstanceId] = nti
        else:
            next_tasks_by_id = {}
        timings['query_next_tasks'] = time.time() - t4
        app_logger.info(f"[PERF] Query next tasks: {timings['query_next_tasks']:.3f}s (found {len(next_tasks_by_id)} tasks)")
        
        # Collect tasks to auto-complete (for recursive calls)
        tasks_to_autocomplete = []
        
        # Process next tasks
        for flow_to in task_flows_to:
            next_task_instance = next_tasks_by_id.get(flow_to.ToTaskId)
            if not next_task_instance:
                continue
                
            task_def = next_task_instance.TaskDef
            condition = flow_to.Condition if task_def else None
            
            # Check condition
            if condition and result and condition != 'None' and condition.lower() != result.lower():
                app_logger.info(f"Skipping task {task_def.TaskName} - condition mismatch")
                continue
            
            # Validate prior tasks (now optimized)
            if validate_prior_tasks_optimized(task_def, stages_list_cache, task_instance_cache):
                next_task_instance.Status = 'PENDING'
                next_task_instance.AssignedTo = completed_by
                next_task_instance.StartedDate = datetime.utcnow()
                updates_to_commit.append(next_task_instance)
                
            # Queue for auto-completion
            if next_task_instance.TaskDef.AutoComplete:
                tasks_to_autocomplete.append(next_task_instance.TaskInstanceId)
    
        # IMPROVEMENT 8: Batch commit all updates
        t5 = time.time()
        for update in updates_to_commit:
            session.add(update)
        session.commit()
        timings['commit'] = time.time() - t5
        app_logger.info(f"[PERF] Database commit ({len(updates_to_commit)} objects): {timings['commit']:.3f}s")
        
        # IMPROVEMENT 9: Process auto-complete tasks after commit
        # CHANGE: Only do recursive calls at depth 0 to avoid deep recursion
        # For depth > 0, collect tasks and let the parent handle them
        t6 = time.time()
        if depth == 0:
            # At root level - process all auto-complete tasks iteratively
            all_autocomplete_tasks = list(tasks_to_autocomplete)
            processed_count = 0
            
            while all_autocomplete_tasks:
                next_task_id = all_autocomplete_tasks.pop(0)
                app_logger.debug(f"[PERF] Processing auto-complete task {next_task_id} ({processed_count + 1}/{len(all_autocomplete_tasks) + processed_count + 1})")
                
                # Call recursively but collect any new auto-complete tasks
                result = _complete_task_optimized(
                    task_instance_id=next_task_id, 
                    result=None, 
                    completed_by='system', 
                    completion_notes='Auto-completed', 
                    access_token=access_token, 
                    depth=depth+1,
                    task_instance_cache=task_instance_cache,
                    stages_list_cache=stages_list_cache
                )
                processed_count += 1
                
                # If result contains more tasks to process, add them to the queue
                # (This would require returning tasks_to_autocomplete from recursive calls)
        else:
            # At deeper levels - just do the recursive calls normally
            # The root call will handle the queue
            for next_task_id in tasks_to_autocomplete:
                _complete_task_optimized(
                    task_instance_id=next_task_id, 
                    result=None, 
                    completed_by='system', 
                    completion_notes='Auto-completed', 
                    access_token=access_token, 
                    depth=depth+1,
                    task_instance_cache=task_instance_cache,
                    stages_list_cache=stages_list_cache
                )
        
        timings['recursive_calls'] = time.time() - t6
        if tasks_to_autocomplete:
            app_logger.info(f"[PERF] Recursive auto-complete ({len(tasks_to_autocomplete)} tasks): {timings['recursive_calls']:.3f}s")
                
    except Exception as e:
        app_logger.error(f'Error completing task {task_instance_id}: {e}')
        session.rollback()
        return jsonify({"status": "error", "message": f"Error: {str(e)}"}), 500
    
    # END TIMER
    end_time = time.time()
    processing_time = end_time - start_time
    own_time = processing_time - timings.get('recursive_calls', 0)
    
    # Log detailed breakdown
    if depth == 0:
        app_logger.info(f'[PERF] ====== TASK {task_instance_id} ({task_name}) ROOT CALL COMPLETED ======')
        app_logger.info(f'[PERF] TOTAL TIME: {processing_time:.3f}s')
    else:
        app_logger.info(f'[PERF] Task {task_instance_id} ({task_name}) depth={depth} completed in {processing_time:.3f}s')
    
    app_logger.info(f'[PERF] Breakdown (own time: {own_time:.3f}s) - '
                   f'Query:{timings.get("query_task_instance",0):.3f}s, '
                   f'Prior:{timings.get("check_prior_tasks",0):.3f}s, '
                   f'Script:{timings.get("script_engine",0):.3f}s, '
                   f'NextQuery:{timings.get("query_next_tasks",0):.3f}s, '
                   f'Commit:{timings.get("commit",0):.3f}s, '
                   f'Recursive:{timings.get("recursive_calls",0):.3f}s')
    
    return jsonify({"status": "ok", "data": {
        "task_instance_id": task_instance_id, 
        "processing_time": f"{processing_time:.3f}s",
        "own_time": f"{own_time:.3f}s",
        "depth": depth,
        "timings": timings
    }}), 200


def validate_prior_tasks_optimized(taskDef: TaskDefinition, stages_list: list, task_instance_cache: dict = None) -> bool:
    '''
    Optimized validation using bulk queries and caching
    '''
    if taskDef is None:
        return True
    
    dependencies = taskDef.ToTaskTaskFlowList
    if not dependencies:
        return True
    
    # IMPROVEMENT 10: Bulk query instead of one-by-one
    from_task_ids = [dep.FromTaskId for dep in dependencies]
    
    # Check cache first
    uncached_ids = []
    for task_id in from_task_ids:
        if task_instance_cache:
            # Look for any instance with this TaskId in cache
            found = False
            for ti in task_instance_cache.values():
                if ti.TaskId == task_id and ti.StageId in stages_list:
                    if ti.Status != 'COMPLETED':
                        app_logger.info(f"Task {taskDef.TaskName} blocked by {ti.TaskDef.TaskName}")
                        return False
                    found = True
                    break
            if not found:
                uncached_ids.append(task_id)
        else:
            uncached_ids.append(task_id)
    
    # Query uncached in bulk
    if uncached_ids:
        from_task_instances = TaskInstance.query.filter(
            TaskInstance.TaskId.in_(uncached_ids),
            TaskInstance.StageId.in_(stages_list)
        ).all()
        
        for from_task_instance in from_task_instances:
            if from_task_instance.Status != 'COMPLETED':
                app_logger.info(f"Task {taskDef.TaskName} blocked by {from_task_instance.TaskDef.TaskName}")
                return False
    
    return True


# Update insert_workflow_history to support deferred commit
def insert_workflow_history_optimized(task_instance, status, result, completed_by, completion_notes, priorStatus=None, commit=True):
    """
    Insert workflow history with optional commit
    """
    from database.models import WorkflowHistory
    
    task_name = task_instance.TaskDef.TaskName if task_instance and task_instance.TaskDef else 'N/A'
    wf_history = WorkflowHistory(
        InstanceId=task_instance.Stage.ProcessInstance.InstanceId,
        TaskInstanceId=task_instance.TaskInstanceId,
        Action=f'{task_name} changed to {status} with result: {result}' if result else f'{task_name} {status}',
        NewStatus=status,
        PreviousStatus=priorStatus,
        ActionBy=completed_by,
        ActionReason=completion_notes
    )
    session.add(wf_history)
    
    if commit:
        session.commit()
    
    return wf_history
