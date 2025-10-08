from datetime import datetime
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
    def start_workflow():
        """
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

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
        process_name = data.get('process_name', "OU Application Init")
        application_id = data.get('application_id', '1')
        started_by = data.get('started_by', 'admin')
        priority = data.get('priority', 'NORMAL')  # Default to 'Normal' if not provided
        app_logger.debug(f'Starting workflow: {process_name} for application_id: {application_id} by {started_by} with priority {priority}')
        return _start_workflow(process_name, int(application_id), started_by, priority)

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

    @app.route('/complete_task', methods=['POST','OPTIONS'])
    @admin_required()
    def complete_task():
        """
        Complete a task in the workflow {task_instance_id:int, result:str, completed_by:str, completion_notes:str}
        # Example PowerShell command to complete a task in the workflow
        $body = @{
            task_instance_id = 102
            result = "Approved"
            completed_by = "user1"
            completion_notes = "Task completed successfully"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri "http://localhost:5656/complete_task" -Method POST -Body $body -ContentType "application/json"
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200       
        
        data = request.get_json()
        task_instance_id = data.get("task_instance_id")
        completed_by = data.get("completed_by",'system')
        completion_notes = data.get("completion_notes",'Complete Task via API')
        result = data.get("result", None)
        app_logger.debug(f'Completing task: {task_instance_id} by {completed_by}')
        return _complete_task(task_instance_id, result, completed_by, completion_notes)

    

    @app.route('/application_message', methods=['POST','OPTIONS'])
    def application_message():
        """
        Send a message to a task in the workflow
        """
        data = request.get_json()
        message = data.get("message")
        applicationID = data.get("application_id")
        fromUser = data.get("from_user")
        toUser = data.get("to_user")
        priority = data.get("priority", 'NORMAL')
        message_type = data.get("message_type", 'Standard')

        app_logger.debug(f'Sending message to application: {applicationID}')

        # Find the task instance
        application = WFApplication.query.filter_by(ApplicationID=applicationID).first()
        if not application:
                app_logger.error(f'Application not found: {applicationID}')
                return jsonify({"status": "error", "message": f"Application {applicationID} not found"}), 404

        # Add the message to the task instance
        message = WFApplicationMessage(
                ApplicationID=applicationID,
                MessageText=message,
                FromUser=fromUser,
                ToUser=toUser,
                MessageType=message_type,
                Priority=priority
        )
        session.add(message)
        session.commit()

        app_logger.info(f'Message for application {applicationID} added')
        return jsonify({"status": "ok", "data": {"application_id": applicationID}}), 200

    @app.route('/process_message', methods=['POST','OPTIONS'])
    def process_message():
        """
        Send a message to a task in the workflow
        """
        data = request.get_json()
        message = data.get("message")
        processID = data.get("process_id")
        fromUser = data.get("from_user")
        toUser = data.get("to_user")
        subject = data.get("subject")
        priority = data.get("priority", 'NORMAL')
        message_type = data.get("message_type", 'Standard')

        app_logger.debug(f'Sending message to task: {processID}')

        # Find the task instance
        process_instance = ProcessInstance.query.filter_by(ProcessID=processID).first()
        if not process_instance:
                app_logger.error(f'ProcessInstance not found: {processID}')
                return jsonify({"status": "error", "message": f"ProcessInstance {processID} not found"}), 404

        # Add the message to the task instance
        message = ProcessMessage(
                ProcessID=processID,
                MessageBody=message,
                FromUser=fromUser,
                Subject=subject,
                ToUser=toUser,
                MessageType=message_type,
                Priority=priority
        )
        session.add(message)
        session.commit()

        app_logger.info(f'Message added to ProcessInstance: {processID} for process {process_instance.Name}')
        return jsonify({"status": "ok", "data": {"process_id": processID}}), 200

    @app.route('/assign_task', methods=['POST','OPTIONS'])
    def assign_task():
        """
        Assign a user to a task in the workflow
        """
        data = request.get_json()
        task_instance_id = data.get("task_instance_id")
        user_id = data.get("user_id")

        app_logger.debug(f'Assigning user {user_id} to task: {task_instance_id}')

        # Find the task instance
        task_instance = TaskInstance.query.filter_by(InstanceId=task_instance_id).first()
        if not task_instance:
            app_logger.error(f'TaskInstance not found: {task_instance_id}')
            return jsonify({"status": "error", "message": f"TaskInstance {task_instance_id} not found"}), 404

        # Assign the user to the task
        task_instance.AssignedTo = user_id
        session.add(task_instance)
        session.commit()

        wf_history = WorkflowHistory(
            InstanceId=task_instance.InstanceId,
            TaskInstanceId=task_instance_id,
            Action='AssignTask',
            NewStatus='COMPLETED',
            ActionBy= 'system', # Session.current_user
            ActionReason=f'assigned user {user_id} to task {task_instance_id}'
        )
        session.add(wf_history)
        session.commit()
        app_logger.info(f'User {user_id} assigned to TaskInstance: {task_instance_id}')
        return jsonify({"status": "ok", "data": {"task_instance_id": task_instance_id}}), 200

    
    @app.route('/validate_tasks', methods=['GET','OPTIONS'])
    #@jwt_required()
    def validate_tasks():   
        '''
        Validate tasks in the workflow
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

    @app.route('/get_application_tasks', methods=['GET','OPTIONS'])
    def get_application_tasks():
        """
        Retrieves all of the application tasks within their stages for a given application_id
        
        Returns JSON data only - use: (Invoke-WebRequest -Uri 'http://localhost:5656/get_application_tasks?application_id=1' -Method GET).Content | ConvertFrom-Json

        $response = Invoke-WebRequest -Uri 'http://localhost:5656/get_application_tasks?application_id=1' -Method GET
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        data = request.args if request.args else {}
        application_id = data.get('application_id', None)
        if application_id is None:
            return jsonify({"status": "error", "message": "application_id is required"}), 400
        
        app_logger.info('Retrieving NCRC dashboard data')
        # Implement your logic to retrieve and return the NCRC dashboard data:
        
        app_obj = WFApplication.query.filter_by(ApplicationID=application_id).first()
        if not app_obj:
            return jsonify({"status": "error", "message": "Application not found"}), 404    
        
        process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
        if process_instance is None:
            return jsonify({"status": "error", "message": "Process instance not found or workflow not started"}), 404
        result = {}
        result['process_instance'] = process_instance.to_dict() if process_instance else {}
        stage_list = process_instance.StageInstanceList if process_instance else []
        result['stages'] = {}
        #[stage.to_dict() if stage else {} for stage in stage_list]
        for stage in stage_list:
            result['stages'][stage.Lane.LaneName] = {
                "stage_info": stage.to_dict() if stage else {},
                "tasks": []
            }
            tasks = stage.TaskInstanceList if stage else []
            for task in tasks:
                result['stages'][stage.Lane.LaneName]['tasks'].append(task.to_dict() if task else {})
        return jsonify({"status": "ok", "data": result}), 200

        # ==================================================
        #        END WORKFLOW ENDPOINTS (Flask)
        # ==================================================
   
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
    start_task_id = task_definition.TaskId if task_definition else None
    app_logger.info(f'Start TaskDefinition TaskId: {start_task_id}') 
    if start_task_id is None:
            raise Exception(f'Start Task definition not found for process: {process_name}')
    
    process_instance_id = process_instance.InstanceId
    # Insert into ProcessInstances
    app_logger.info(f'New ProcessInstance InstanceId: {process_instance_id}')

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

            task_definition = TaskDefinition.query.filter_by(LaneId=lane.LaneId).order_by(TaskDefinition.Sequence).all() # LaneId=lane.LaneId
            task_instances = []
            for task_definition in task_definition:
                    app_logger.info(f'Create TaskInstance from TaskDefinition: {task_definition.TaskName}')
                    status = 'NEW' #if task_definition.TaskType != 'START' else 'COMPLETED'
                    task_instance = TaskInstance(
                            TaskId=task_definition.TaskId,
                            StageId=stage_instance.StageInstanceId,
                            Status=status,
                            CreatedDate=datetime.utcnow(),
                            CreatedBy=started_by,
                        
                    )
                    session.add(task_instance)
                    session.commit()
                    app_logger.info(f'Created TaskInstance: {task_definition.TaskName}')
                    task_instances.append(task_instance)
                    if task_instance.TaskId == start_task_id:
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
    _complete_task(start_instance_id, 'Started', 'system', 'Workflow started')
    role_assignment = models.RoleAssigment(
        ApplicationId=application.ApplicationID,
        Role="DISPATCH",
        Assignee=started_by,
        CreatedDate=datetime.utcnow()
    )
    session.add(role_assignment)
    session.commit()
    app_logger.info(f'Role DISPATCH assigned to {started_by} for application {application.ApplicationID}')
    return jsonify({"status": "ok", "data": {"process_instance_id": process_instance_id}}), 200     



def _complete_task(task_instance_id: int, result: str = None, completed_by: str = 'system', completion_notes: str = 'Complete Task via API'):
        # Find the task instance
        task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
        if not task_instance:
            app_logger.error(f'TaskInstance not found: {task_instance_id}')
            return jsonify({"status": "error", "message": "TaskInstance not found"}), 404

        # Go To TaskFlow from TaskId and check to see if all the prior states are completed
        task_def = task_instance.TaskDef
        if not task_def:
            app_logger.error(f'TaskDefinition not found: {task_instance.TaskId}')
            return jsonify({"status": "error", "message": "TaskDefinition not found"}), 404

        if task_instance.Status != 'PENDING' and task_def.TaskType != 'START':
            app_logger.error(f'Cannot complete task {task_instance_id}. Task is not PENDING -> {task_instance.Status}.')
            return jsonify({"status": "error", "message": f"Cannot complete task. Task is not Pending  -> {task_instance.Status}."}), 400
        
        task_name = task_def.TaskName
        stages_list = get_stage_list(task_instance)
        app_logger.info(f'Completing TaskInstance: {task_instance_id} - {task_name}')
        task_flows_from = task_def.ToTaskTaskFlowList or []
        task_flows_to = task_def.TaskFlowList or []
        # Check if all prior tasks are completed
        if task_def.TaskType != "START":
            for tf in task_flows_from:
                prior_task_id = tf.FromTaskId
                prior_task_instance = TaskInstance.query.filter(
                    TaskInstance.TaskInstanceId == prior_task_id
                    #,TaskInstance.StageId.in_(stages_list)
                ).first()
                if prior_task_instance and prior_task_instance.Status != 'COMPLETED':
                    app_logger.error(f'Cannot complete task {task_name} - {task_instance_id}. Prior task {prior_task_id} is not COMPLETED.')
                    return jsonify({"status": "error", "message": f"Cannot complete task. Prior task {prior_task_id} is not COMPLETED."}), 400
            #result = ScriptEngine.run_script(task_def.PreCompletionScript, {"task_instance": task_instance, "session": session})      
        
        task_instance.Status = 'COMPLETED'
        task_instance.CompletedDate = datetime.utcnow()
        task_instance.Result = result
        session.add(task_instance)
        try:
            session.commit()
            session.flush()
        except Exception as e:
            app_logger.error(f'Error completing task {task_instance_id}: {e}')
            session.rollback()
            return jsonify({"status": "error", "message": "Error completing task"}), 500

        ## Get the workflow history
        wf_history = WorkflowHistory(
            InstanceId= task_instance.Stage.ProcessInstance.InstanceId,
            TaskInstanceId=task_instance.TaskInstanceId,
            Action=f'{task_name}  COMPLETED with result: {result}' if result else f'{task_name} COMPLETED',
            NewStatus='COMPLETED',
            ActionBy=completed_by,
            ActionReason=completion_notes
        )
        session.add(wf_history)
        session.commit()
        session.flush()
        
        # Start the next tasks
        for flow_to in task_flows_to:
            next_task_id = flow_to.ToTaskId
            next_task_instance = TaskInstance.query.filter(TaskInstance.TaskId == next_task_id,
                                                            TaskInstance.StageId.in_(stages_list)).first()
            task_def = next_task_instance.TaskDef if next_task_instance else None
            condition = flow_to.Condition
            if task_def and task_def.TaskType == 'CONDITION' and \
                 condition and condition != 'None' and result and condition.lower() != result.lower():
                app_logger.info(f"Skipping dependency check for task {task_def.TaskName} because condition '{condition}' does not match result '{result}'.")
                continue  # Skip this dependency as the condition does not match the result
            elif next_task_instance and next_task_instance.Status == 'NEW' and validate_prior_tasks(task_def, stages_list, result):
                next_task_instance.Status = 'PENDING'
                next_task_instance.StartedDate = datetime.utcnow()
                session.add(next_task_instance)    
                session.commit()
            if next_task_instance and next_task_instance.TaskDef.AutoComplete and validate_prior_tasks(next_task_instance.TaskDef, stages_list, result):
                _complete_task(next_task_instance.TaskInstanceId, result,  'system', 'Auto-completed')

                
        app_logger.info(f'Task completed:{task_name} - {task_instance_id}')
        return jsonify({"status": "ok", "data": {"task_instance_id": task_instance_id}}), 200

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
            from_task_def = dependency.FromTaskId
            condition = dependency.Condition
            if taskDef.TaskType == 'CONDITION' and condition and condition != 'None' and result and condition.lower() != result.lower():
                app_logger.info(f"Skipping dependency check for task {taskDef.TaskName} because condition '{condition}' does not match result '{result}'.")
                continue  # Skip this dependency as the condition does not match the result
            from_task_instance = TaskInstance.query.filter(TaskInstance.TaskId == from_task_def, 
                                                           TaskInstance.StageId.in_(stages_list)).first()
            if from_task_instance and from_task_instance.Status != 'COMPLETED' and taskDef.TaskType not in ['START']:
                app_logger.info(f"Cannot proceed with task {taskDef.TaskName} because dependency task {from_task_instance.TaskDef.TaskName} is not COMPLETED.")
                return False
        return True

def get_stage_list(taks_instance: TaskInstance) -> list:
    '''
    Get the list of stages for a given task instance.
    '''
    stages = []
    if taks_instance is None:
        return stages
    
    stage_instances = taks_instance.Stage.ProcessInstance.StageInstanceList
    for stage_instance in stage_instances:
        stages.append(stage_instance.StageInstanceId)
    return stages

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
            _complete_task_with_session(thread_session, start_instance_id, 'Started', 'system', 'Workflow started')
        
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

def _complete_task_with_session(thread_session, task_instance_id: int, result: str = None, completed_by: str = 'system', completion_notes: str = 'Complete Task via API'):
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