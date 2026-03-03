from functools import wraps
from config.config import Args
from config.config import Config
from flask import jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import verify_jwt_in_request
from database.models import TaskFlow, TaskDefinition, StageDefinition
import logging
import safrs
import json
import os

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def write_to_file(file_name, result):
    filename = f"{_project_dir}/database/{file_name}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir

    @app.route('/insert_task_flow', methods=['GET',"OPTIONS"])
    def insert_task_flow():
        """
        Add a new task flow between tasks
        
        Args:
            from_task: Source task name (None for start flows)
            to_task: Destination task name (required)
            condition: Optional condition for the flow
            
            Test with:
            curl -X GET "http://localhost:5000/insert_task_flow?from_task=TaskA&to_task=TaskB&condition=Approved" -H "accept: application/json"
        $response = Invoke-WebRequest -Uri 'http://localhost:5656/insert_task_flow?from_task=START&to_task=END&condition=COMPLETE' -Method GET
        $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
        $jsonString | ConvertFrom-Json
            
        Returns:
            Dictionary with flow information or error details
        """
        result = {}
        data = request.args
        from_task_name = data.get("from_task")
        to_task_name = data.get("to_task")
        condition = data.get("condition", None)
        if not from_task_name and not to_task_name:
            return jsonify({
                'ErrorMessage': "Both from_task and to_task must be provided",
                'ErrorType': 'TaskFlowError'
            }), 400
        
        try:
            from_task_id = None
            
            # Look up the ToTask ID (required)
            to_task = TaskDefinition.query.filter_by(TaskName=to_task_name).first()
            if to_task is None:
                raise ValueError(f"ToTask not found: {to_task_name}")
            
            
            to_task_id = to_task.TaskId
            # Look up the FromTask ID (optional for start flows)
            if from_task_name is not None:
                from_task = TaskDefinition.query.filter_by(TaskName=from_task_name).first()
                if from_task is None:
                    raise ValueError(f"FromTask not found: {from_task_name}")
                from_task_id = from_task.TaskId
            
            # Check if flow already exists
            task_flow = TaskFlow.query.filter_by(FromTaskId=from_task_id, ToTaskId=to_task_id).first()
            if task_flow:
                raise ValueError(f"Flow already exists from '{from_task_name}' to '{to_task_name}'")
            
            # Insert the new flow
            task_flow = TaskFlow(
                FromTaskId=from_task_id,
                ToTaskId=to_task_id,
                Condition=condition,
                IsDefault=False
            )
            session.add(task_flow)
            session.commit()
            
            result = {
                'FromTaskName': from_task,
                'ToTaskName': to_task,
                'FlowId': task_flow.FlowId,
                'FromTaskId': from_task_id,
                'ToTaskId': to_task_id,
                'Condition': condition,
                'Message': 'Flow added successfully'
            }
            print(result)
            
        except Exception as e:
            session.rollback()
            return jsonify({
                'ErrorMessage': str(e),
                'ErrorType': 'TaskFlowError'
            }), 400
        return jsonify(result), 200

    @app.route('/display_task_definitions', methods=['GET',"OPTIONS"])
    def display_task_definitions():
        """
        Display all existing task definitions for debugging
        There is Only one Task START and one Task END

            curl -X GET "http://localhost:5000/display_task_definitions -H "accept: application/json"
            $response = Invoke-WebRequest -Uri 'http://localhost:5656/display_task_definitions' -Method GET
            $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
            $jsonString | ConvertFrom-Json
        
        """
        app_logger.info("Displaying all task definitions")
        result = ""
        stages = StageDefinition.query.order_by(StageDefinition.StageId).all()
        for stage in stages:
            #result.append({
            #    "LaneName": lane.LaneName,
            #    'LaneId': lane.LaneId
            #})
            result += f"\n-- Stage: {stage.StageName} (ID: {stage.StageId})\n"
            result += 'INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)\n'
            result += 'VALUES\n'
            app_logger.info(f"Stage: {stage.StageName} (ID: {stage.StageId})")   
            task_defs = TaskDefinition.query.filter_by(LaneId=stage.StageId).order_by(TaskDefinition.TaskId).all()
            for task in task_defs:
                '''
                INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
                VALUES
                (1, 'Start_Application_Submitted', 'START', 'COMPLETION', 1, 1, 'SYSTEM', NULL, 'Application submitted and ready for admin review', 1,'system'),

                '''
                result += f"({task.ProcessId}, '{task.TaskName}', '{task.TaskType}', '{task.TaskCategory}', {task.Sequence}, {task.LaneId}, '{task.AssigneeRole}', {task.EstimatedDurationMinutes if task.EstimatedDurationMinutes is not None else 'NULL'}, '{task.Description}', {1 if task.AutoComplete else 0}, '{task.CreatedBy}'),\n"
                app_logger.info({
                    "LaneName": lane.LaneName,
                    'TaskName': task.TaskName,
                    'TaskType': task.TaskType,
                    'TaskCategory': task.TaskCategory,
                    'Sequence': task.Sequence,
                    'LaneId': task.LaneId,
                    'AssigneeRole': task.AssigneeRole,
                    'EstimatedDurationMinutes': task.EstimatedDurationMinutes,
                    'Description': task.Description,
                    'AutoComplete': task.AutoComplete,
                    'CreatedBy': task.CreatedBy
                })
        write_to_file("task_definitions.sql", result)
        return jsonify({'Message': 'Task definitions displayed in logs', 'data': result}), 200

    @app.route('/display_task_flows', methods=['GET',"OPTIONS"])
    def display_task_flows():
        """
        Display all existing task flows for debugging
        There is Only one Task START and one Task END
        Each TaskFlow can have an optional Condition

            curl -X GET "http://localhost:5000/display_task_flows -H "accept: application/json"
            $response = Invoke-WebRequest -Uri 'http://localhost:5656/display_task_flows' -Method GET
            $jsonString = [System.Text.Encoding]::UTF8.GetString($response.Content)
            $jsonString | ConvertFrom-Json
        
        """
        start_task = TaskDefinition.query.filter_by(TaskType='START').first()
        end_task = TaskDefinition.query.filter_by(TaskType='END').first()
        if start_task is None or end_task is None:
            app_logger.error("START or END task not defined in TaskDefinition")
            return jsonify({
                'ErrorMessage': "START or END task not defined in TaskDefinition",
                'ErrorType': 'TaskFlowError'
            }), 400
            
        app_logger.info(f"Start Task: {start_task.TaskName} (ID: {start_task.TaskId})")
        app_logger.info(f"End Task: {end_task.TaskName} (ID: {end_task.TaskId})")
        result = ""
        stages = StageDefinition.query.order_by(StageDefinition.StageId).all()
        for stage in stages:
            result += "\n"
            app_logger.info(f"Stage: {stage.StageName} (ID: {stage.StageId})")   
            result += f"-- Stage: {stage.StageName}\n\n"
            task_defs = TaskDefinition.query.filter_by(StageDefinitionId=stage.StageId).order_by(TaskDefinition.TaskId).all()
            for task in task_defs:
                #app_logger.info(f"Lane:{lane.LaneName}  Task: {task.TaskName} (ID: {task.TaskId}, Type: {task.TaskType})")
                flows = TaskFlow.query.filter((TaskFlow.FromTaskId == task.TaskId)).all() #| (TaskFlow.ToTaskId == task.TaskId
                for flow in flows:
                    from_task_name = flow.FromTask.TaskName 
                    to_task_name = flow.ToTask.TaskName 
                    condition = flow.Condition or "None"
                    app_logger.info(f"FlowId: {flow.FlowId}, From: {from_task_name}, To: {to_task_name}, Condition: {condition}")
                    #result.append({
                    #    "LaneName": lane.LaneName,
                    #    'FromTaskName': from_task_name,
                    #    'ToTaskName': to_task_name,
                    #    'Condition': condition
                    #})
                    result += f"EXEC sp_add_flow @from_name = '{from_task_name}', @to_name = '{to_task_name}', @condition = '{condition}'; \n"
            result += "\nGO\n"
        write_to_file("task_flows.sql", result)
        return jsonify({'Message': 'Task flows displayed in logs', 'data': result}), 200

 