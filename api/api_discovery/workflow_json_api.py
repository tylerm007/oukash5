"""
Workflow JSON API Endpoints

Provides REST endpoints for retrieving nested JSON workflow hierarchy data.
Returns ProcessDefinitions -> LaneDefinitions -> TaskDefinitions -> TaskFlow in JSON format.
"""

from flask import request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt
import logging
import safrs
from functools import wraps
from config.config import Args
from database.workflow_json_queries import WorkflowJSONQuery

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators=[]):
    """Add workflow JSON API endpoints."""
    
    def admin_required():
        """Support option to bypass security."""
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                if Args.instance.security_enabled == False:
                    return fn(*args, **kwargs)
                from flask_jwt_extended import verify_jwt_in_request
                verify_jwt_in_request(True)  # must be issued if security enabled
                return fn(*args, **kwargs)
            return decorator
        return wrapper

    @app.route('/workflow_json', methods=['GET', 'OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def get_workflow_hierarchy_json():
        """
        Get complete workflow hierarchy as nested JSON.
        
        Query Parameters:
            process_id (optional): Filter by specific process ID
            include_inactive (optional): Include inactive processes (default: false)
            simple (optional): Return simplified structure (default: false)
        
        Returns nested JSON structure:
        [
            {
                "ProcessId": 1,
                "ProcessName": "Application Workflow",
                "ProcessVersion": "1.0",
                "ProcessDescription": "Main application processing workflow",
                "ProcessIsActive": true,
                "Lanes": [
                    {
                        "LaneId": 1,
                        "LaneName": "Initial Review",
                        "LaneDescription": "First stage review",
                        "Tasks": [
                            {
                                "TaskId": 1,
                                "TaskName": "Application Intake",
                                "TaskType": "START",
                                "Sequence": 1,
                                "OutgoingFlows": [...],
                                "IncomingFlows": [...]
                            }
                        ]
                    }
                ],
                "AllTaskFlows": [...]
            }
        ]
        
        Test with:
        GET /workflow_json
        GET /workflow_json?process_id=1
        GET /workflow_json?simple=true
        GET /workflow_json?include_inactive=true
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        try:
            # Get query parameters
            process_id = request.args.get('process_id', type=int)
            include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
            simple = request.args.get('simple', 'false').lower() == 'true'
            
            app_logger.info(f"📊 Workflow JSON request: process_id={process_id}, "
                           f"include_inactive={include_inactive}, simple={simple}")
            
            # Execute appropriate query
            if simple:
                workflow_data = WorkflowJSONQuery.get_simple_workflow_json(process_id)
                response_type = "simple_hierarchy"
            else:
                workflow_data = WorkflowJSONQuery.get_workflow_hierarchy_json(process_id, include_inactive)
                response_type = "complete_hierarchy"
            
            # Get summary stats
            stats = WorkflowJSONQuery.get_process_summary_stats()
            
            response = {
                "status": "success",
                "response_type": response_type,
                "total_processes": len(workflow_data),
                "summary_stats": stats,
                "data": workflow_data,
                "query_parameters": {
                    "process_id": process_id,
                    "include_inactive": include_inactive,
                    "simple": simple
                }
            }
            
            app_logger.info(f"✅ Returned {len(workflow_data)} processes in {response_type} format")
            return jsonify(response), 200
            
        except Exception as e:
            app_logger.error(f"❌ Error in workflow JSON endpoint: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "error_type": "workflow_json_query_error"
            }), 500

    @app.route('/workflow_json/<int:process_id>', methods=['GET', 'OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def get_specific_workflow_json(process_id: int):
        """
        Get specific workflow hierarchy as nested JSON.
        
        Path Parameters:
            process_id: The process ID to retrieve
            
        Query Parameters:
            simple (optional): Return simplified structure (default: false)
            include_inactive (optional): Include inactive processes (default: false)
        
        Test with:
        GET /workflow_json/1
        GET /workflow_json/1?simple=true
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        try:
            simple = request.args.get('simple', 'false').lower() == 'true'
            include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
            
            app_logger.info(f"📊 Specific workflow JSON request for process {process_id}")
            
            # Execute query for specific process
            if simple:
                workflow_data = WorkflowJSONQuery.get_simple_workflow_json(process_id)
            else:
                workflow_data = WorkflowJSONQuery.get_workflow_hierarchy_json(process_id, include_inactive)
            
            if not workflow_data:
                return jsonify({
                    "status": "not_found",
                    "message": f"Process {process_id} not found or not active",
                    "process_id": process_id
                }), 404
            
            # Return single process data
            process_data = workflow_data[0]
            
            response = {
                "status": "success",
                "process_id": process_id,
                "response_type": "simple_hierarchy" if simple else "complete_hierarchy",
                "data": process_data
            }
            
            app_logger.info(f"✅ Returned process {process_id} with "
                           f"{len(process_data.get('Lanes', []))} lanes")
            return jsonify(response), 200
            
        except Exception as e:
            app_logger.error(f"❌ Error getting workflow {process_id}: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "process_id": process_id,
                "error_type": "specific_workflow_error"
            }), 500

    @app.route('/workflow_stats', methods=['GET', 'OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def get_workflow_statistics():
        """
        Get workflow summary statistics.
        
        Returns:
        {
            "status": "success",
            "stats": {
                "TotalProcesses": 5,
                "TotalLanes": 15,
                "TotalTasks": 52,
                "TotalFlows": 72,
                "ActiveProcesses": 4,
                "ConditionalFlows": 12,
                "AvgLaneDurationDays": 5.2,
                "AvgTaskDurationMinutes": 45.8
            }
        }
        
        Test with:
        GET /workflow_stats
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        try:
            app_logger.info("📊 Workflow statistics request")
            
            stats = WorkflowJSONQuery.get_process_summary_stats()
            
            response = {
                "status": "success",
                "stats": stats,
                "description": {
                    "TotalProcesses": "Total number of process definitions",
                    "TotalLanes": "Total number of lane definitions",
                    "TotalTasks": "Total number of task definitions", 
                    "TotalFlows": "Total number of task flows",
                    "ActiveProcesses": "Number of active processes",
                    "ConditionalFlows": "Number of flows with conditions",
                    "AvgLaneDurationDays": "Average lane duration in days",
                    "AvgTaskDurationMinutes": "Average task duration in minutes"
                }
            }
            
            app_logger.info(f"✅ Returned workflow statistics: {stats}")
            return jsonify(response), 200
            
        except Exception as e:
            app_logger.error(f"❌ Error getting workflow statistics: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "error_type": "workflow_stats_error"
            }), 500

    @app.route('/workflow_json/export', methods=['GET', 'OPTIONS'])
    @cross_origin()
    @admin_required()
    @jwt_required()
    def export_workflow_json():
        """
        Export all workflow data as downloadable JSON file.
        
        Query Parameters:
            format (optional): 'simple' or 'complete' (default: complete)
            include_inactive (optional): Include inactive processes (default: false)
        
        Returns: JSON file download
        
        Test with:
        GET /workflow_json/export
        GET /workflow_json/export?format=simple
        """
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        try:
            from flask import make_response
            import json as json_module
            from datetime import datetime
            
            format_type = request.args.get('format', 'complete')
            include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
            
            app_logger.info(f"📥 Workflow export request: format={format_type}")
            
            # Get workflow data
            if format_type == 'simple':
                workflow_data = WorkflowJSONQuery.get_simple_workflow_json()
            else:
                workflow_data = WorkflowJSONQuery.get_workflow_hierarchy_json(None, include_inactive)
            
            # Create export package
            export_data = {
                "export_info": {
                    "export_date": datetime.utcnow().isoformat(),
                    "format": format_type,
                    "include_inactive": include_inactive,
                    "total_processes": len(workflow_data)
                },
                "summary_stats": WorkflowJSONQuery.get_process_summary_stats(),
                "workflow_data": workflow_data
            }
            
            # Create downloadable response
            response = make_response(json_module.dumps(export_data, indent=2, default=str))
            response.headers['Content-Type'] = 'application/json'
            response.headers['Content-Disposition'] = f'attachment; filename=workflow_export_{format_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            app_logger.info(f"✅ Exported {len(workflow_data)} processes as {format_type} JSON")
            return response
            
        except Exception as e:
            app_logger.error(f"❌ Error exporting workflow JSON: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e),
                "error_type": "workflow_export_error"
            }), 500

    app_logger.info("🔗 Workflow JSON API endpoints registered:")
    app_logger.info("   GET  /workflow_json - Get workflow hierarchy JSON")
    app_logger.info("   GET  /workflow_json/<process_id> - Get specific workflow JSON")
    app_logger.info("   GET  /workflow_stats - Get workflow statistics")
    app_logger.info("   GET  /workflow_json/export - Export workflow data as JSON file")