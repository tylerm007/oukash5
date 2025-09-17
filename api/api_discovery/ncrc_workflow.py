from asyncio import Task
from datetime import datetime
from multiprocessing import process
from unicodedata import category
from database.models import ProcessDefinition, TaskDefinition, ProcessInstance, WFApplication, WorkflowHistory, StageInstance, TaskInstance, LaneDefinition, TaskFlow , ProcessMessage, WFApplicationMessage
from flask import request, jsonify, session
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
import logging
import safrs
from config.config import Args
from config.config import Config

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass

    # ==================================================
    #        WORKFLOW ENDPOINTS (Flask)
    # ==================================================
    @app.route('/start_workflow', methods=['POST','OPTIONS'])
    @jwt_required()
    def start_workflow():
        """
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with PowerShell POST:

        $body = @{
                process_name = "Application Workflow"
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
        process_name = data.get('process_name', "OU Certification Workflow")
        application_id = data.get('application_id', '1')
        started_by = data.get('started_by', 'admin')
        priority = data.get('priority', 'NORMAL')  # Default to 'Normal' if not provided
        app_logger.debug(f'Starting workflow: {process_name} for application_id: {application_id} by {started_by} with priority {priority}')
        return _start_workflow(process_name, int(application_id), started_by, priority)

    def _start_workflow(process_name:str, application_id:int, started_by:str, priority:str):

        application = WFApplication.query.filter_by(ApplicationID=application_id).first()
        if not application:
                raise Exception(f'Application not found: {application_id}') 
        # Get ProcessId
        process_def = ProcessDefinition.query.filter_by(ProcessName=process_name, IsActive=True).first()
        if not process_def:
                raise Exception(f'Process definition not found: {process_name}') 
        process_id = process_def.ProcessId
        print(f'ProcessDefinition ProcessId: {process_id}')

 
        # Create new Process InstanceId for this Application
        process_instance = ProcessInstance.query.filter_by(ApplicationId=application_id).first()
        #if process_instance is None:
                 # Get StartTaskId
        row = TaskDefinition.query.filter_by(ProcessId=process_id, TaskType='EVENT', TaskCategory='START').order_by(TaskDefinition.Sequence).first()
        start_task_id = row.TaskId if row else None
        print(f'Start TaskDefinition TaskId: {start_task_id}') 
        if start_task_id is None:
                raise Exception(f'Start Task definition not found for process: {process_name}')
        process_instance = ProcessInstance(
            ProcessId=process_id,
            ApplicationId=int(application_id),
            CurrentTaskId=start_task_id,
            StartedBy=started_by,
            Priority=priority
        )
        session.add(process_instance)
        session.commit()
        #else:
        #    return jsonify({"status": "error", "message": f"Workflow already started for application {application_id}"}), 400
             
        process_instance_id = process_instance.InstanceId
        # Insert into ProcessInstances
        app_logger.info(f'New ProcessInstance InstanceId: {process_instance_id}')


        # TODO - use TaskFlow to only create starting tasks?
        LaneDefinitions = LaneDefinition.query.filter_by(ProcessId=process_id).all()
        for lane in LaneDefinitions:
                print(f'LaneDefinition: {lane.LaneName}')
                stage_instance = StageInstance(
                        ProcessInstanceId=process_instance_id,
                        LaneId=lane.LaneId,
                        Status='NEW',
                        CreatedBy=started_by
                )
                session.add(stage_instance)
                session.commit()

                rows = TaskDefinition.query.filter_by(LaneId=lane.LaneId).order_by(TaskDefinition.Sequence).all() # LaneId=lane.LaneId
                task_instances = []
                for row in rows:
                        print(f'TaskDefinition: {row.TaskName}')
                        status = 'Pending' # if row.TaskCategory != 'START' else 'Completed'
                        task_instance = TaskInstance(
                                TaskId=row.TaskId,
                                StageId=stage_instance.StageInstanceId,
                                Status=status,
                                CreatedDate=datetime.utcnow(),
                                CreatedBy=started_by,
                            
                        )
                        session.add(task_instance)
                        session.commit()
                        app_logger.info(f'Created TaskInstance: {row.TaskName}')
                        task_instances.append(task_instance)
                        wf_history = WorkflowHistory(
                                InstanceId=process_instance_id,
                                TaskInstanceId=task_instance.TaskInstanceId,
                                Action=row.TaskName,
                                NewStatus='ACTIVE',
                                ActionBy=started_by,
                                ActionReason=f'New application id: {application_id} Task added to workflow'
                        )
                        session.add(wf_history)
                        session.commit()
                        
        #link_task(task_instances)
        #set_start_task(task_instances)        
        return jsonify({"status": "ok", "data": {"process_instance_id": process_instance_id}}), 200     
    
    @app.route('/complete_task', methods=['POST','OPTIONS'])
    def complete_task():
        """
        Complete a task in the workflow
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200       
        
        data = request.get_json()
        task_instance_id = data.get("taskId")
        completed_by = data.get("completed_by",'system')
        completion_notes = data.get("completion_notes",'testing')

        app_logger.debug(f'Completing task: {task_instance_id} by {completed_by}')

        # Find the task instance
        task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance_id).first()
        if not task_instance:
            app_logger.error(f'TaskInstance not found: {task_instance_id}')
            return jsonify({"status": "error", "message": "TaskInstance not found"}), 404

        # Go To TaskFlow from TaskId and check to see if all the prior states are completed
        task_def = TaskDefinition.query.filter_by(TaskId=task_instance.TaskId).first()
        if not task_def:
            app_logger.error(f'TaskDefinition not found: {task_instance.TaskId}')
            return jsonify({"status": "error", "message": "TaskDefinition not found"}), 404

        task_flows_from = task_def.ToTaskTaskFlowList
        task_flows_to = task_def.TaskFlowList
        # Check if all prior tasks are completed
        for tf in task_flows_from:
            prior_task_id = tf.FromTaskId
            prior_task_instance = TaskInstance.query.filter_by(TaskInstanceId=prior_task_id).first()
            if prior_task_instance and prior_task_instance.Status != 'Completed':
                app_logger.error(f'Cannot complete task {task_instance_id}. Prior task {prior_task_id} is not completed.')
                return jsonify({"status": "error", "message": f"Cannot complete task. Prior task {prior_task_id} is not completed."}), 400
        #result = ScriptEngine.run_script(task_def.PreCompletionScript, {"task_instance": task_instance, "session": session})      
        # Update the task instance status
        task_instance.Status = 'Completed'
        task_instance.CompletedAt = datetime.utcnow()
        task_instance.CompletedBy = completed_by
        task_instance.CompletionNotes = completion_notes
        session.commit()
        ## Get the workflow history
        wf_history = WorkflowHistory(
            InstanceId= task_instance.Stage.ProcessInstance.InstanceId,
            TaskInstanceId=task_instance.TaskInstanceId,
            Action='COMPLETE',
            NewStatus='COMPLETED',
            ActionBy=completed_by,
            ActionReason=completion_notes
        )
        session.add(wf_history)
        session.commit()
        #result = ScriptEngine.run_script(task_def.PostCompletionScript, {"task_instance": task_instance, "session": session})
        # Start the next tasks
        for flow_to in task_flows_to:
            next_task_id = flow_to.ToTaskId
            next_task_instance = TaskInstance.query.filter_by(TaskInstanceId=task_instance.TaskInstanceId, TaskId=next_task_id).first()
            if next_task_instance and next_task_instance.Status == 'Pending':
                next_task_instance.Status = 'InProgress'
                session.add(next_task_instance)
                session.commit()
        app_logger.info(f'Task completed: {task_instance_id}')
        return jsonify({"status": "ok", "data": {"task_instance_id": task_instance_id}}), 200

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

        app_logger.debug(f'Sending message to task: {task_instance_id}')

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

    def set_start_task(task_instances: list[TaskInstance]):
        """Set the start task to completed - this will kick off the workflow to pending"""
        for task_instance in task_instances:
            task_def = task_instance.TaskDef
            if task_def and task_def.TaskCategory == 'START':
                new_task = TaskInstance.query.filter_by(TaskInstanceId=task_instance.TaskInstanceId).first()
                new_task.Status = 'Completed'
                new_task.CompletedAt = datetime.utcnow()
                new_task.CompletedBy = 'system'
                session.add(new_task)
                session.commit()
                app_logger.info(f'Start TaskInstance set to Completed: {task_instance.TaskInstanceId}')
                break

    
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
            -Headers @{Authorization = "Bearer <your_jwt_token>"}
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

        # ==================================================
        #        END WORKFLOW ENDPOINTS (Flask)
        # ==================================================
