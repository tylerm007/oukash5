from flask import request, jsonify, session
import logging
import safrs
from database.cache_service import DatabaseCacheService

cache = DatabaseCacheService.get_instance()

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB 
session = db.session 
_project_dir = None

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir
    _project_dir = project_dir
    pass

    @app.route('/visualize_task_flow', methods=['GET','OPTIONS'])
    #@jwt_required()
    def visualize_task_flow():
        '''
        Generate a visual diagram of the task flow for a process
        
        Query Parameters:
            - process_name: Name of the process to visualize (default: "OU Certification Workflow")
            - format: Output format - 'mermaid', 'dot', 'ascii', 'html' (default: 'mermaid')
            - validate: Whether to include validation results (default: false)
            - stats: Whether to include statistics (default: false)
        
        Example:
            GET http://localhost:5656/visualize_task_flow?process_name=OU%20Certification%20Workflow&format=html
            
            PowerShell:
            Invoke-RestMethod -Uri "http://localhost:5656/visualize_task_flow?process_name=OU%20Certification%20Workflow&format=mermaid" -Method GET
        
        Returns:
            json: response with diagram in requested format
        '''
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200
        
        # Import the TaskFlow visualizer
        from tools.task_flow_visualizer import TaskFlowGraph
        
        # Get query parameters
        process_name = request.args.get('process_name', "OU Application Init")
        output_format = request.args.get('format', 'mermaid').lower()
        include_validation = request.args.get('validate', 'false').lower() == 'true'
        include_stats = request.args.get('stats', 'false').lower() == 'true'
        
        if not process_name:
            return jsonify({"status": "error", "message": "process_name is required"}), 400
        
        try:
            # Create the task flow graph
            app_logger.info(f'Generating task flow visualization for process: {process_name}')
            task_flow = TaskFlowGraph(process_name)
            
            # Load data from database
            if not task_flow.load_from_database(session):
                return jsonify({"status": "error", "message": f"Process definition not found: {process_name}"}), 404
            
            # Generate the diagram based on requested format
            if output_format == 'mermaid':
                diagram = task_flow.generate_mermaid_diagram()
            elif output_format == 'dot':
                diagram = task_flow.generate_dot_diagram()
            elif output_format == 'ascii':
                diagram = task_flow.generate_ascii_diagram()
            elif output_format == 'html':
                html_content = task_flow.export_to_html(include_mermaid=True)
                from flask import Response
                return Response(html_content, mimetype='text/html')
            else:
                return jsonify({"status": "error", "message": f"Unsupported format: {output_format}. Use 'mermaid', 'dot', 'ascii', or 'html'"}), 400
            
            # Build response
            response_data = {
                "status": "ok",
                "process_name": process_name,
                "format": output_format,
                "diagram": diagram
            }
            
            # Add statistics if requested
            if include_stats:
                response_data["statistics"] = task_flow.get_statistics()
            
            # Add validation if requested
            if include_validation:
                validation_issues = task_flow.validate_flow()
                response_data["validation"] = {
                    "valid": len(validation_issues) == 0,
                    "issues": validation_issues
                }
            
            app_logger.info(f'Successfully generated {output_format} diagram for process: {process_name}')
            return jsonify(response_data), 200
            
        except Exception as e:
            app_logger.error(f'Error generating task flow visualization: {e}')
            import traceback
            traceback.print_exc()
            return jsonify({"status": "error", "message": str(e)}), 500
