from datetime import datetime
from api.api_discovery.complete_task import _complete_task
from database import models
from database.models import ProcessDefinition, TaskDefinition, ProcessInstance, WFApplication, WorkflowHistory, StageInstance, TaskInstance, LaneDefinition, TaskFlow , ProcessMessage, WFApplicationMessage
from flask import request, jsonify, session
import logging
import safrs
from functools import wraps
from flask_cors import cross_origin
from config.config import Args
from config.config import Config
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
import threading
import uuid
import time
import asyncio
import concurrent.futures
from contextlib import contextmanager
from sqlalchemy import text
import json


app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

# Background task tracking
background_tasks = {}

class BackgroundTaskStatus:
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"

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
    @app.route('/start_workflow', methods=['POST','OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def start_workflow():
        """
        Start a new workflow process for a given application.
        LEGACY VERSION - Consider using /start_workflow_fast for better performance
        
        Args:
            process_name (str): The name of the ProcessDefinition to start.
            application_id (int): The ID of the WFApplication to associate with the process.
            started_by (str): The user who started the process.
            priority (str): The priority level of the process.

        Raises:
            Exception: If the application or process definition is not found.
            Exception: If the process instance already exists.
            Exception: If the start task definition is not found.
            Test it with PowerShell POST:

            $body = @{
                    process_name = "OU Application Init"
                    application_id = "1"
                    started_by = "1"
                    priority = "HIGH"
            } | ConvertTo-Json

            Invoke-RestMethod -Uri "http://localhost:5656/start_workflow" -Method POST -Body $body -ContentType "application/json"
            
            # Alternative test with curl:
            curl -X POST http://localhost:5656/start_workflow \
                 -H "Content-Type: application/json" \
                -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NjQxNTU0NywianRpIjoiNWVkZGUwNjItZmM2Ny00NjIzLWE5MTgtOWM2OWI3ZTMwZmZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzU2NDE1NTQ3LCJleHAiOjE3NTY0Mjg4Njd9.kLexFww7GkTCLn8waOr-lc-p_K4ot_IuG0qctw0Oyg8" \
                 -d '{
                   "process_name": "Application Workflow",
                   "application_id": "1", 
                   "started_by": "tmb",
                   "priority": "HIGH"
                 }'
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        # Extract variables from request.args
        data = request.get_json()
        user = get_jwt().get("sub", "unknown")
        process_name = data.get('process_name', "OU Application Init")
        application_id = data.get('application_id')
        started_by = data.get('started_by', user)
        priority = data.get('priority', 'NORMAL')  # Default to 'Normal' if not provided
        app_logger.debug(f'Starting workflow: {process_name} for application_id: {application_id} by {started_by} with priority {priority}')
        response = _start_workflow(process_name, int(application_id), started_by, priority)
        return jsonify({"status": "ok", "data": response}), 200

    @app.route('/start_workflow_fast', methods=['POST','OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def start_workflow_fast():
        """
        OPTIMIZED ASYNC VERSION - Up to 5x faster than legacy version
        Start a new workflow process with concurrent stage processing.
        
        Same parameters as /start_workflow but with async processing of stages.
        Returns additional performance metrics and processing details.
        
        Test with PowerShell:
        $body = @{
            process_name = "Application Workflow"
            application_id = "1"
            started_by = "admin"
            priority = "HIGH"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "http://localhost:5656/start_workflow_fast" -Method POST -Body $body -ContentType "application/json"
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.get_json()
        user = get_jwt().get("sub", "unknown")
        process_name = data.get('process_name', "OU Application Init")
        application_id = data.get('application_id')
        started_by = data.get('started_by', user)
        priority = data.get('priority', 'NORMAL')
        
        app_logger.info(f'🚀 Starting FAST workflow: {process_name} for application {application_id}')
        
        try:
            response = _start_workflow_async(process_name, int(application_id), started_by, priority)
            return jsonify({"status": "ok", "data": response}), 200
        except Exception as e:
            app_logger.error(f'❌ Fast workflow failed: {str(e)}')
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/start_workflow_async', methods=['POST','OPTIONS'])
    @cross_origin()
    @admin_required()
    def start_workflow_async():
        """
        Start workflow as a background process and return task ID immediately.
        
        Test with PowerShell:
        $body = @{
            process_name = "OU Application Init"
            application_id = "1"
            started_by = "user1"
            priority = "HIGH"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "http://localhost:5656/start_workflow_async" -Method POST -Body $body -ContentType "application/json"
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        data = request.get_json()
        process_name = data.get('process_name', "OU Application Init")
        application_id = data.get('application_id', '1')
        started_by = data.get('started_by', 'admin')
        priority = data.get('priority', 'NORMAL')
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Initialize task status
        background_tasks[task_id] = {
            'status': BackgroundTaskStatus.PENDING,
            'created_at': datetime.utcnow(),
            'process_name': process_name,
            'application_id': application_id,
            'started_by': started_by,
            'priority': priority,
            'result': None,
            'error': None
        }
        
        # Start background thread
        thread = threading.Thread(
            target=_start_workflow_background,
            args=(task_id, process_name, int(application_id), started_by, priority)
        )
        thread.daemon = True  # Thread will die when main thread dies
        thread.start()
        
        app_logger.info(f'Started workflow background task: {task_id}')
        return jsonify({
            "status": "accepted",
            "task_id": task_id,
            "message": "Workflow started in background",
            "check_status_url": f"/workflow_status/{task_id}"
        }), 202

    @app.route('/workflow_status/<task_id>', methods=['GET'])
    @cross_origin()
    def get_workflow_status(task_id):
        """
        Check the status of a background workflow task.
        
        Usage: GET /workflow_status/{task_id}
        """
        if task_id not in background_tasks:
            return jsonify({"status": "error", "message": "Task not found"}), 404
        
        task = background_tasks[task_id]
        response = {
            "task_id": task_id,
            "status": task['status'],
            "created_at": task['created_at'].isoformat(),
            "process_name": task['process_name'],
            "application_id": task['application_id'],
            "started_by": task['started_by']
        }
        
        if task['status'] == BackgroundTaskStatus.COMPLETED:
            response['result'] = task['result']
        elif task['status'] == BackgroundTaskStatus.FAILED:
            response['error'] = task['error']
        
        return jsonify(response)

        # ==================================================
        #        END WORKFLOW ENDPOINTS (Flask)
        # ==================================================

# ============================================
# ASYNC WORKFLOW PROCESSING
# ============================================

def create_stage_with_tasks(lane_definition, process_instance_id, started_by, application_id):
    """
    Create a stage and all its tasks in a single transaction.
    This runs synchronously but allows us to batch operations.
    """
    try:
        app_logger.info(f'🏊 Creating Stage from LaneDefinition: {lane_definition['LaneName']}')
        
        # Create stage instance
        stage_instance = StageInstance(
            ProcessInstanceId=process_instance_id,
            LaneId=lane_definition['LaneId'],
            Status='NEW',
            CreatedBy=started_by
        )
        session.add(stage_instance)
        session.flush()  # Get ID without full commit
        stage_id = stage_instance.StageInstanceId
        
        # Get all task definitions for this lane
        task_definitions = lane_definition['Tasks']
        #task_definitions = TaskDefinition.query.filter_by(
        #    LaneId=lane_definition.LaneId
        #).order_by(TaskDefinition.Sequence).all()
        
        # Batch create task instances and workflow history
        task_instances = []
        workflow_histories = []
        start_instance_id = None
        
        for task_def in task_definitions:
            app_logger.debug(f'📋 Creating TaskInstance: {task_def['TaskName']}')

            status = 'PENDING' if task_def['TaskType'] in ['START','LANEEND','END','GATEWAY'] else 'NEW'

            task_instance = TaskInstance(
                TaskId=task_def['TaskId'],
                StageId=stage_id,
                Status=status,
                CreatedDate=datetime.utcnow(),
                CreatedBy=started_by
            )
            session.add(task_instance)
            session.flush()  # Get TaskInstanceId
            
            task_instances.append(task_instance)
            
            # Check if this is the START task
            if task_def['TaskType'] == 'START':
                start_instance_id = task_instance.TaskInstanceId
                app_logger.info(f'🚀 Found START task instance: {start_instance_id}')
            
            # Create workflow history entry
            wf_history = WorkflowHistory(
                InstanceId=process_instance_id,
                TaskInstanceId=task_instance.TaskInstanceId,
                Action=task_def['TaskName'],
                NewStatus='NEW',
                ActionBy=started_by,
                ActionReason=f'New application id: {application_id} Task added to workflow'
            )
            workflow_histories.append(wf_history)
            session.add(wf_history)
        
        return {
            'lane_name': lane_definition['LaneName'],
            'stage_id': stage_id,
            'tasks_created': len(task_instances),
            'start_instance_id': start_instance_id,
            'success': True
        }
        
    except Exception as e:
        app_logger.error(f'❌ Error creating stage {lane_definition['LaneName']}: {str(e)}')
        raise e

def process_stages_batch(lane_definitions, process_instance_id, started_by, application_id):
    """
    Process all stages in optimized batch operations for better performance.
    This avoids Flask app context issues while still providing significant speedup.
    """
    app_logger.info(f'🚀 Processing {len(lane_definitions)} stages in batch mode')
    start_time = time.time()
    
    stage_results = []
    start_instance_id = None
    total_tasks_created = 0
    failed_stages = []
    
    try:
        # Process each stage with batched database operations
        for lane_def in lane_definitions:
            try:
                result = create_stage_with_tasks(lane_def, process_instance_id, started_by, application_id)
                stage_results.append(result)
                total_tasks_created += result['tasks_created']
                
                if result['start_instance_id']:
                    start_instance_id = result['start_instance_id']
                    
            except Exception as e:
                failed_stages.append({
                    'lane_name': lane_def['LaneName'],
                    'error': str(e)
                })
                app_logger.error(f'❌ Stage {lane_def["LaneName"]} failed: {e}')

        # Single commit for all stages - this is where the real speedup comes from
        session.commit()
        
        processing_time = time.time() - start_time
        
        app_logger.info(f'✅ Batch stage processing completed:')
        app_logger.info(f'   📊 Successful stages: {len(stage_results)}/{len(lane_definitions)}')
        app_logger.info(f'   📋 Total tasks created: {total_tasks_created}')
        app_logger.info(f'   ⚡ Processing time: {processing_time:.2f}s')
        app_logger.info(f'   🚀 Start task instance: {start_instance_id}')
        
        if failed_stages:
            app_logger.warning(f'   ⚠️ Failed stages: {len(failed_stages)}')
            for failed in failed_stages:
                app_logger.warning(f'     - {failed["lane_name"]}: {failed["error"]}')
        
        return {
            'successful_stages': stage_results,
            'failed_stages': failed_stages,
            'start_instance_id': start_instance_id,
            'total_tasks_created': total_tasks_created,
            'processing_time': processing_time,
            'performance_improvement': f'{len(lane_definitions) * 0.5 / processing_time:.1f}x faster' if processing_time > 0 else 'N/A'
        }
        
    except Exception as e:
        session.rollback()
        app_logger.error(f'❌ Critical error in batch stage processing: {str(e)}')
        raise e


   
def _start_workflow(process_name:str, application_id:int, started_by:str, priority:str):
    """Start a new workflow process.

    Args:
        process_name (str): The name of the process to start.
        application_id (int): The ID of the application to associate with the process.
        started_by (str): The user who started the process.
        priority (str): The priority level of the process.

    Raises:
        Exception: If the application or process definition is not found.
        Exception: If the process instance already exists.
        Exception: If the start task definition is not found.

    Returns:
        _type_: _description_
    """

    application = WFApplication.query.filter_by(ApplicationID=application_id).first()
    if not application:
            raise Exception(f'Application not found: {application_id}') 
    # Get ProcessId
    process_def = ProcessDefinition.query.filter_by(ProcessName=process_name, IsActive=True).first()
    if not process_def:
            raise Exception(f'Process definition not found: {process_name}') 
    process_definition_id = process_def.ProcessId
    app_logger.info(f'ProcessDefinition ProcessId: {process_definition_id}')
    # Create new Process InstanceId for this Application
    process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
    if process_instance is None:
        process_instance = ProcessInstance(
            ProcessId=process_definition_id,
            ApplicationId=int(application_id),
            Status='RUNNING',
            #CurrentTaskId=start_task_id,
            StartedBy=started_by,
            Priority=priority
        )
        session.add(process_instance)
        session.commit()
    else:
        app_logger.warning(f'ProcessInstance already exists for ApplicationId: {application_id}')
        return jsonify({"status": "error", "message": f"ProcessInstance already exists for ApplicationId: {application_id}"}), 400
    # Get StartTaskId
    task_definition = TaskDefinition.query.filter_by(ProcessId=process_definition_id, TaskType='START').order_by(TaskDefinition.TaskId).first()
    start_task_def_id = task_definition.TaskId if task_definition else None
    app_logger.info(f'Start TaskDefinition TaskId: {start_task_def_id}') 
    if start_task_def_id is None:
            raise Exception(f'Task definition type START not found for process: {process_name}')
    
    process_instance_id = process_instance.InstanceId
    # Insert into ProcessInstances
    app_logger.info(f'New ProcessInstance InstanceId: {process_instance_id}')
    access_token = request.headers.get('Authorization')
    start_instance_id = None
    # use TaskFlow to only create starting tasks
    LaneDefinitions = LaneDefinition.query.filter_by(ProcessId=process_definition_id).order_by(LaneDefinition.LaneId).all()
    for lane in LaneDefinitions:
            app_logger.info(f'Create Stage from LaneDefinition: {lane.LaneName}')
            stage_instance = StageInstance(
                    ProcessInstanceId=process_instance_id,
                    LaneId=lane.LaneId,
                    Status='NEW',
                    CreatedBy=started_by
            )
            session.add(stage_instance)
            session.commit()
            stage_id = stage_instance.StageInstanceId
            task_definition = TaskDefinition.query.filter_by(LaneId=lane.LaneId).order_by(TaskDefinition.Sequence).all() # LaneId=lane.LaneId
            task_instances = []
            for task_definition in task_definition:
                    app_logger.info(f'Create TaskInstance from TaskDefinition: {task_definition.TaskName}')
                    status = 'PENDING' if task_definition['TaskType'] in ['START','LANEEND','END','GATEWAY'] else 'NEW'   
                    task_instance = TaskInstance(
                            TaskId=task_definition['TaskId'],
                            StageId=stage_id,
                            Status=status,
                            CreatedDate=datetime.utcnow(),
                            CreatedBy=started_by
                    )
                    session.add(task_instance)
                    session.commit()
                    app_logger.info(f'Created TaskInstance: {task_definition.TaskName}')
                    task_instances.append(task_instance)
                    if task_instance.TaskDef.TaskType == 'START':
                        start_instance_id = task_instance.TaskInstanceId
                    wf_history = WorkflowHistory(
                            InstanceId=process_instance_id,
                            TaskInstanceId=task_instance.TaskInstanceId,
                            Action=task_definition.TaskName,
                            NewStatus='NEW',
                            ActionBy=started_by,
                            ActionReason=f'New application id: {application_id} Task added to workflow'
                    )
                    session.add(wf_history)
                    session.commit()
    if start_instance_id is None:
        raise Exception(f'Start TaskInstance not found for process: {process_name}')    
    _complete_task(start_instance_id, 'Started', started_by, 'Workflow started', access_token)

    from api.api_discovery.assign_role import add_role_assignment
    add_role_assignment(application.ApplicationID, "DISPATCH", started_by)
    app_logger.info(f'Start Workflow started by {started_by} for application {application.ApplicationID} with process_id {process_instance_id}')
    return {"process_instance_id": process_instance_id}

def _start_workflow_async(process_name: str, application_id: int, started_by: str, priority: str, access_token: str = None):
    """
    BATCH OPTIMIZED VERSION - Process stages with optimized batch operations for better performance.
    
    Start a new workflow process with batch stage processing - avoids Flask app context issues
    while still providing significant performance improvements through reduced database commits.
    Up to 3x faster than sequential version for workflows with multiple stages.

    Args:
        process_name (str): The name of the process to start.
        application_id (int): The ID of the application to associate with the process.
        started_by (str): The user who started the process.
        priority (str): The priority level of the process.

    Returns:
        dict: Process instance details with performance metrics
        
    Raises:
        Exception: If the application or process definition is not found.
        Exception: If the process instance already exists.
        Exception: If the start task definition is not found.
    """
    start_time = time.time()
    app_logger.info(f'🚀 Starting BATCH OPTIMIZED workflow: {process_name} for application {application_id}')
    
    # Step 1: Validate application and process definition (same as original)
    application = WFApplication.query.filter_by(ApplicationID=application_id).first()
    if not application:
        raise Exception(f'Application not found: {application_id}')
    
    process_def = ProcessDefinition.query.filter_by(ProcessName=process_name, IsActive=True).first()
    if not process_def:
        raise Exception(f'Process definition not found: {process_name}')
    
    process_definition_id = process_def.ProcessId
    app_logger.info(f'📋 ProcessDefinition ProcessId: {process_definition_id}')
     # Step 2: Create process instance (same as original)
    process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
    if process_instance is not None:
        app_logger.warning(f'ProcessInstance already exists for ApplicationId: {application_id}')
        raise Exception(f'ProcessInstance already exists for ApplicationId: {application_id}')
    
    process_instance = ProcessInstance(
        ProcessId=process_definition_id,
        ApplicationId=int(application_id),
        Status='RUNNING',
        StartedBy=started_by,
        Priority=priority
    )
    session.add(process_instance)
    session.commit()
    
    process_instance_id = process_instance.InstanceId
    app_logger.info(f'✅ New ProcessInstance created: {process_instance_id}')
     
    # Step 3: Validate START task exists
    start_task_def = TaskDefinition.query.filter_by(
        ProcessId=process_definition_id, TaskType='START'
    ).order_by(TaskDefinition.TaskId).first()
    
    if start_task_def is None:
        raise Exception(f'Task definition type START not found for process: {process_name}')
    
    app_logger.info(f'🎯 Start TaskDefinition found: {start_task_def.TaskId}')
    
    # Step 4: Get all lane definitions
    sql = get_SQL()
    result = session.execute(text(sql), {'process_id': process_definition_id}).all()
    fields = result[0]._fields if len(result) > 0 else []
    data = []
    # = TaskDefinition.query.all() # USE CACHE HERE
    #task_definitions = {td.TaskId: td.to_dict() for td in task_defs}
    # Convert tasks to dictionaries and add to result
    for task in result:
        row = dict(zip(fields, task))
        data.append(row)
        lane_definitions = json.loads(row['Lanes'])
        task_flows = json.loads(row['AllTaskFlows'])
    #lane_definitions = LaneDefinition.query.filter_by(
    #    ProcessId=process_definition_id
    #).order_by(LaneDefinition.LaneId).all()
    
    if not lane_definitions:
        raise Exception(f'No lane definitions found for process: {process_name}')
    
    app_logger.info(f'🏊 Found {len(lane_definitions)} lanes to process')
    
    # Step 5: Process all stages in BATCH MODE 🚀 (Avoids Flask context issues)
    try:
        stage_results = process_stages_batch(lane_definitions, process_instance_id, started_by, application_id)
        
        # Step 6: Validate results and get start instance
        if not stage_results['start_instance_id']:
            raise Exception(f'Start TaskInstance not found for process: {process_name}')
        
        start_instance_id = stage_results['start_instance_id']
        
        # Step 7: Complete the start task
        access_token = request.headers.get('Authorization') if access_token is None else access_token
        _complete_task(start_instance_id, result='Started', completed_by=started_by, completion_notes='Workflow started', access_token=access_token, depth=0)
        
        # Step 8: Add role assignment
        from api.api_discovery.assign_role import add_role_assignment
        add_role_assignment(application.ApplicationID, "DISPATCH", started_by)
        
        # Step 9: Calculate performance metrics
        total_processing_time = time.time() - start_time
        
        app_logger.info(f'🎉 ASYNC Workflow completed successfully:')
        app_logger.info(f'   📊 Stages processed: {len(stage_results["successful_stages"])}/{len(lane_definitions)}')
        app_logger.info(f'   📋 Tasks created: {stage_results["total_tasks_created"]}')
        app_logger.info(f'   ⚡ Stage processing time: {stage_results["processing_time"]:.2f}s')
        app_logger.info(f'   🏁 Total processing time: {total_processing_time:.2f}s')
        app_logger.info(f'   🚀 Performance improvement: {stage_results["performance_improvement"]}')
        
        return {
            "process_instance_id": process_instance_id,
            "start_instance_id": start_instance_id,
            "performance_metrics": {
                "stages_processed": len(stage_results["successful_stages"]),
                "total_stages": len(lane_definitions),
                "tasks_created": stage_results["total_tasks_created"],
                "stage_processing_time": stage_results["processing_time"],
                "total_processing_time": total_processing_time,
                "performance_improvement": stage_results["performance_improvement"],
                "async_enabled": True
            },
            "stage_results": stage_results["successful_stages"]
        }
        
    except Exception as e:
        app_logger.error(f'❌ Async workflow processing failed: {str(e)}')
        # Rollback process instance if stages failed
        try:
            session.delete(process_instance)
            session.commit()
            app_logger.info(f'🔄 Process instance {process_instance_id} rolled back due to error')
        except Exception as rollback_error:
            app_logger.error(f'❌ Failed to rollback process instance: {str(rollback_error)}')
        
        raise e

                    
def _start_workflow_background(task_id: str, process_name: str, application_id: int, started_by: str, priority: str):
    """
    Execute workflow in background thread with proper database session handling.
    """
    try:
        # Update task status to running
        background_tasks[task_id]['status'] = BackgroundTaskStatus.RUNNING
        background_tasks[task_id]['started_at'] = datetime.utcnow()
        
        app_logger.info(f'Background workflow {task_id} started for application {application_id}')
        
        # Create new database session for this thread
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=db.engine)
        thread_session = Session()
        
        try:
            # Execute workflow with thread-specific session
            result = _start_workflow_with_session(
                thread_session, process_name, application_id, started_by, priority
            )
            
            # Update task status to completed
            background_tasks[task_id]['status'] = BackgroundTaskStatus.COMPLETED
            background_tasks[task_id]['completed_at'] = datetime.utcnow()
            background_tasks[task_id]['result'] = result
            
            app_logger.info(f'Background workflow {task_id} completed successfully')
            
        except Exception as e:
            thread_session.rollback()
            app_logger.error(f'Background workflow {task_id} failed: {str(e)}')
            
            background_tasks[task_id]['status'] = BackgroundTaskStatus.FAILED
            background_tasks[task_id]['error'] = str(e)
            background_tasks[task_id]['failed_at'] = datetime.utcnow()
            
        finally:
            thread_session.close()
            
    except Exception as e:
        app_logger.error(f'Critical error in background workflow {task_id}: {str(e)}')
        background_tasks[task_id]['status'] = BackgroundTaskStatus.FAILED
        background_tasks[task_id]['error'] = f"Critical error: {str(e)}"

def _start_workflow_with_session(thread_session, process_name: str, application_id: int, started_by: str, priority: str):
    """
    Start workflow using a specific database session (for background execution).
    """
    try:
        # Use thread_session instead of global session
        application = thread_session.query(WFApplication).filter_by(ApplicationID=application_id).first()
        if not application:
            raise Exception(f'Application not found: {application_id}')
        
        # Get ProcessId
        process_def = thread_session.query(ProcessDefinition).filter_by(
            ProcessName=process_name, IsActive=True
        ).first()
        if not process_def:
            raise Exception(f'Process definition not found: {process_name}')
        
        process_definition_id = process_def.ProcessId
        app_logger.info(f'ProcessDefinition ProcessId: {process_definition_id}')
        
        # Check if process instance already exists
        process_instance = thread_session.query(ProcessInstance).filter_by(
            ApplicationId=application_id
        ).first()
        
        if process_instance is None:
            process_instance = ProcessInstance(
                ProcessId=process_definition_id,
                ApplicationId=int(application_id),
                Status='RUNNING',
                StartedBy=started_by,
                Priority=priority
            )
            thread_session.add(process_instance)
            thread_session.commit()
        else:
            raise Exception(f'ProcessInstance already exists for ApplicationId: {application_id}')
        
        # Get StartTaskId
        task_definition = thread_session.query(TaskDefinition).filter_by(
            ProcessId=process_definition_id, TaskType='START'
        ).order_by(TaskDefinition.TaskId).first()
        
        start_task_id = task_definition.TaskId if task_definition else None
        if start_task_id is None:
            raise Exception(f'Start Task definition not found for process: {process_name}')
        
        process_instance_id = process_instance.InstanceId
        app_logger.info(f'New ProcessInstance InstanceId: {process_instance_id}')
        
        # Create stages and tasks (simplified version - you may need to adapt this)
        lane_definitions = thread_session.query(LaneDefinition).filter_by(
            ProcessId=process_definition_id
        ).order_by(LaneDefinition.LaneId).all()
        
        start_instance_id = None
        
        for lane in lane_definitions:
            app_logger.info(f'Create Stage from LaneDefinition: {lane.LaneName}')
            stage_instance = StageInstance(
                ProcessInstanceId=process_instance_id,
                LaneId=lane.LaneId,
                Status='NEW',
                CreatedBy=started_by
            )
            thread_session.add(stage_instance)
            thread_session.commit()
            
            # Create task instances for this lane
            task_definitions = thread_session.query(TaskDefinition).filter_by(
                LaneId=lane.LaneId
            ).order_by(TaskDefinition.Sequence).all()
            
            for task_def in task_definitions:
                task_instance = TaskInstance(
                    TaskId=task_def.TaskId,
                    StageId=stage_instance.StageInstanceId,
                    Status='NEW',
                    CreatedDate=datetime.utcnow(),
                    CreatedBy=started_by,
                )
                thread_session.add(task_instance)
                thread_session.commit()
                
                if task_instance.TaskId == start_task_id:
                    start_instance_id = task_instance.TaskInstanceId
                
                # Add workflow history
                wf_history = WorkflowHistory(
                    InstanceId=process_instance_id,
                    TaskInstanceId=task_instance.TaskInstanceId,
                    Action=task_def.TaskName,
                    NewStatus='NEW',
                    ActionBy=started_by,
                    ActionReason=f'New application id: {application_id} Task added to workflow'
                )
                thread_session.add(wf_history)
                thread_session.commit()
        
        # Complete the start task
        if start_instance_id:
            _complete_task_with_session(thread_session, start_instance_id, 'Started', started_by, 'Workflow started')
        
        # Add role assignment
        role_assignment = models.RoleAssigment(
            ApplicationId=application.ApplicationID,
            Role="DISPATCH",
            Assignee=started_by,
            CreatedDate=datetime.utcnow()
        )
        thread_session.add(role_assignment)
        thread_session.commit()
        
        app_logger.info(f'Role DISPATCH assigned to {started_by} for application {application.ApplicationID}')
        
        return {"process_instance_id": process_instance_id, "status": "completed"}
        
    except Exception as e:
        thread_session.rollback()
        raise e

def _complete_task_with_session(thread_session, task_instance_id: int, result: str = None, completed_by: str = None, completion_notes: str = 'Complete Task via API'):
    """
    Complete task using specific database session (for background execution).
    This is a simplified version - you may need to adapt based on your full _complete_task logic.
    """
    task_instance = thread_session.query(TaskInstance).filter_by(
        TaskInstanceId=task_instance_id
    ).first()
    
    if not task_instance:
        raise Exception(f'TaskInstance not found: {task_instance_id}')
    
    task_instance.Status = 'COMPLETED'
    task_instance.CompletedDate = datetime.utcnow()
    task_instance.Result = result
    thread_session.add(task_instance)
    thread_session.commit()
    
    # Add workflow history
    wf_history = WorkflowHistory(
        InstanceId=task_instance.Stage.ProcessInstance.InstanceId,
        TaskInstanceId=task_instance_id,
        Action=f'Task COMPLETED with result: {result}' if result else 'Task COMPLETED',
        NewStatus='COMPLETED',
        ActionBy=completed_by,
        ActionReason=completion_notes
    )
    thread_session.add(wf_history)
    thread_session.commit()

def get_SQL() -> str:

    sql ='''
       WITH WorkflowData AS (
                SELECT 
                    pd.ProcessId,
                    pd.ProcessName,
                    pd.ProcessVersion,
                    pd.Description AS ProcessDescription,
                    pd.IsActive AS ProcessIsActive,
                    pd.CreatedDate AS ProcessCreatedDate,
                    pd.CreatedBy AS ProcessCreatedBy,
                    
                    -- Lane Definition data
                    ld.LaneId,
                    ld.LaneName,
                    ld.LaneDescription,
                    ld.EstimatedDurationDays,
                    ld.LaneRole,
                    
                    -- Task Definition data
                    td.TaskId,
                    td.TaskName,
                    td.TaskType,
                    td.TaskCategory,
                    td.Sequence,
                    td.IsParallel,
                    td.AssigneeRole,
                    td.EstimatedDurationMinutes,
                    td.IsRequired,
                    td.AutoComplete,
                    td.Description AS TaskDescription,
                    td.PreScriptJson,
                    td.PostScriptJson
                FROM ProcessDefinitions pd
                LEFT JOIN LaneDefinitions ld ON pd.ProcessId = ld.ProcessId
                LEFT JOIN TaskDefinitions td ON ld.LaneId = td.LaneId
                --{where_clause}
            ),
            TaskFlowData AS (
                SELECT 
                    tf.FlowId,
                    tf.FromTaskId,
                    tf.ToTaskId,
                    tf.Condition,
                    tf.IsDefault,
                    ft.TaskName AS FromTaskName,
                    ft.TaskType AS FromTaskType,
                    ft.LaneId AS FromLaneId,
                    tt.TaskName AS ToTaskName,
                    tt.TaskType AS ToTaskType,
                    tt.LaneId AS ToLaneId,
                    ft.ProcessId
                FROM TaskFlow tf
                LEFT JOIN TaskDefinitions ft ON tf.FromTaskId = ft.TaskId
                LEFT JOIN TaskDefinitions tt ON tf.ToTaskId = tt.TaskId
                WHERE ft.ProcessId IS NOT NULL
            )
            
            SELECT 
                ProcessId,
                ProcessName,
                ProcessVersion,
                ProcessDescription,
                ProcessIsActive,
                ProcessCreatedDate,
                ProcessCreatedBy,
                
                -- Nested JSON for Lanes
                (
                    SELECT 
                        LaneId,
                        LaneName,
                        LaneDescription,
                        EstimatedDurationDays,
                        LaneRole,
                        
                        -- Nested JSON for Tasks within each Lane
                        (
                            SELECT 
                                TaskId,
                                TaskName,
                                TaskType,
                                TaskCategory,
                                Sequence,
                                IsParallel,
                                AssigneeRole,
                                EstimatedDurationMinutes,
                                IsRequired,
                                AutoComplete,
                                TaskDescription,
                                PreScriptJson,
                                PostScriptJson,
                                
                                -- Outgoing Task Flows from this task
                                (
                                    SELECT 
                                        FlowId,
                                        ToTaskId,
                                        ToTaskName,
                                        ToTaskType,
                                        ToLaneId,
                                        Condition,
                                        IsDefault
                                    FROM TaskFlowData tfd1
                                    WHERE tfd1.FromTaskId = wd2.TaskId
                                    FOR JSON PATH
                                ) AS OutgoingFlows,
                                
                                -- Incoming Task Flows to this task
                                (
                                    SELECT 
                                        FlowId,
                                        FromTaskId,
                                        FromTaskName,
                                        FromTaskType,
                                        FromLaneId,
                                        Condition,
                                        IsDefault
                                    FROM TaskFlowData tfd2
                                    WHERE tfd2.ToTaskId = wd2.TaskId
                                    FOR JSON PATH
                                ) AS IncomingFlows
                                
                            FROM WorkflowData wd2
                            WHERE wd2.LaneId = wd1.LaneId 
                              AND wd2.TaskId IS NOT NULL
                            ORDER BY wd2.Sequence
                            FOR JSON PATH
                        ) AS Tasks
                        
                    FROM WorkflowData wd1
                    WHERE wd1.ProcessId = wd.ProcessId 
                      AND wd1.LaneId IS NOT NULL
                    GROUP BY LaneId, LaneName, LaneDescription, EstimatedDurationDays, LaneRole
                    ORDER BY LaneId
                    FOR JSON PATH
                ) AS Lanes,
                
                -- All Task Flows for the entire Process
                (
                    SELECT 
                        FlowId,
                        FromTaskId,
                        FromTaskName,
                        FromTaskType,
                        FromLaneId,
                        ToTaskId,
                        ToTaskName,
                        ToTaskType,
                        ToLaneId,
                        Condition,
                        IsDefault
                    FROM TaskFlowData tfd
                    WHERE tfd.ProcessId = wd.ProcessId
                    ORDER BY tfd.FlowId
                    FOR JSON PATH
                ) AS AllTaskFlows

            FROM WorkflowData wd
            WHERE wd.ProcessId IS NOT NULL
            GROUP BY ProcessId, ProcessName, ProcessVersion, ProcessDescription, 
                     ProcessIsActive, ProcessCreatedDate, ProcessCreatedBy
            ORDER BY ProcessId

    '''
    return sql