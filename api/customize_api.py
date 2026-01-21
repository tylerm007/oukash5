import logging
import api.system.api_utils as api_utils
import safrs
from flask import request, jsonify
from safrs import jsonapi_rpc
from database import models
from sqlalchemy import text
import json


# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger = logging.getLogger(__name__)

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

def expose_services(app, api, project_dir, swagger_host: str, PORT: str):
    """ Customize API - new end points for services 
    
        Brief background: see readme_customize_api.md

        Your Code Goes Here
    
    """
    
    app_logger.debug("api/customize_api.py - expose custom services")

    from api.api_discovery.auto_discovery import discover_services
    discover_services(app, api, project_dir, swagger_host, PORT)

    @app.route('/plant_details', methods=['GET','OPTIONS'], strict_slashes=False)
    def plant_details():
        """
        Illustrates: 
        
        * #als: "Raw" SQLAlchemy table queries (non-mapped objects), by manual code

        PS> Invoke-RestMethod -Uri "http://localhost:5656/plant_details?plant_id=1"

        Returns:
            json: response
        """
        from database import models
        plant_id = request.args.get('plant_id',2539001)
        
        #Security.set_user_sa()  # an endpoint that requires no auth header (see also @bypass_security)
        if plant_id is None:
            return jsonify('plant_id is required'), 400
        plant = models.PLANTTB.query.filter(models.PLANTTB.PLANT_ID == plant_id).first()
        if plant is None:
            return jsonify(f'Plant not found for plant_id {plant_id}'), 400
        
        address = models.PLANTADDRESSTB.query.filter(models.PLANTADDRESSTB.PLANT_ID == plant_id).first()
        owns = models.OWNSTB.query.filter(models.OWNSTB.PLANT_ID == plant_id).all()
        for own in owns:
            usedin_list = own.USEDIN1TBList
            produced_in_list = own.ProducedIn1TbList
        result = { "plant": plant.to_dict(), 
                    "address": address.to_dict() if address else None,
                    "owns": [ own.to_dict() for own in owns ],
                    "used_in": [ used_in.to_dict() for used_in in usedin_list ],
                    "produced_in": [ produced_in.to_dict() for produced_in in produced_in_list ]
                    }  
        return jsonify({ "success": True, "result":  result})

    @app.route('/stop')
    def stop():  # test it with: http://localhost:5656/stop?msg=API stop - Stop API Logic Server
        """
        Use this to stop the server from the Browser.

        See: https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """

        import os, signal

        if not os.getenv('APILOGICPROJECT_STOP_OK'):
            return jsonify({ "success": False, "message": "Shutdown not enabled" })

        msg = request.args.get('msg')
        app_logger.info(f'\nStopped server: {msg}\n')

        os.kill(os.getpid(), signal.SIGINT)
        return jsonify({ "success": True, "message": "Server is shutting down..." })

    @app.route('/update_task_script', methods=['POST'], strict_slashes=False)
    def update_task_script():
        """
        Update PostScriptJson for a task definition using stored procedure.
        
        Request body:
        {
            "task_name": "Review Application",
            "script": {"action": "validate", "fields": ["company", "contact"]}
        }
        
        PowerShell test:
        $body = @{
            task_name = "Review Application"
            script = @{
                action = "validate"
                fields = @("company", "contact")
                required = $true
            }
        } | ConvertTo-Json -Depth 3

        Invoke-RestMethod -Uri "http://localhost:5656/update_task_script" -Method POST -Body $body -ContentType "application/json"
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"status": "error", "message": "No JSON data provided"}), 400
            
            task_name = data.get('task_name')
            script = data.get('script')
            
            if not task_name:
                return jsonify({"status": "error", "message": "task_name is required"}), 400
            
            # Convert script dict to JSON string if needed
            if isinstance(script, dict):
                script_json = json.dumps(script)
            elif isinstance(script, str):
                script_json = script
            else:
                script_json = '{}' if script is None else str(script)
            
            app_logger.info(f"Updating script for task: {task_name}")
            
            # Execute stored procedure
            result = safrs.DB.session.execute(
                text('EXEC sp_InsertScript @task_name = :task_name, @script = :script'),
                {"task_name": task_name, "script": script_json}
            )
            
            # Get the result
            row = result.fetchone()
            if row:
                response = {
                    "status": row.Status.lower(),
                    "message": row.Message,
                    "task_name": row.TaskName,
                    "tasks_found": getattr(row, 'TasksFound', 0),
                    "tasks_updated": getattr(row, 'TasksUpdated', 0)
                }
                
                # Add task_id if available (single task update)
                if hasattr(row, 'TaskId') and row.TaskId:
                    response["task_id"] = row.TaskId
                
                status_code = 200 if row.Status.upper() == 'SUCCESS' else 400
            else:
                response = {
                    "status": "error",
                    "message": "No response from stored procedure"
                }
                status_code = 500
            
            safrs.DB.session.commit()
            return jsonify(response), status_code
            
        except Exception as e:
            safrs.DB.session.rollback()
            app_logger.error(f"Error updating task script: {e}")
            return jsonify({
                "status": "error", 
                "message": f"Database error: {str(e)}"
            }), 500

    @app.route('/get_task_script/<task_name>', methods=['GET'], strict_slashes=False)
    def get_task_script(task_name):
        """
        Get the current PostScriptJson for a task.
        
        Usage: GET /get_task_script/Review%20Application
        
        PowerShell test:
        Invoke-RestMethod -Uri "http://localhost:5656/get_task_script/Review%20Application" -Method GET
        """
        try:
            result = safrs.DB.session.execute(
                text('SELECT TaskId, TaskName, PostScriptJson FROM TaskDefinitions WHERE TaskName = :task_name'),
                {"task_name": task_name}
            )
            
            row = result.fetchone()
            if row:
                script_content = row.PostScriptJson
                
                # Try to parse JSON if it's a string
                try:
                    if isinstance(script_content, str):
                        parsed_script = json.loads(script_content)
                    else:
                        parsed_script = script_content
                except (json.JSONDecodeError, TypeError):
                    parsed_script = script_content
                
                return jsonify({
                    "status": "success",
                    "task_id": row.TaskId,
                    "task_name": row.TaskName,
                    "script": parsed_script,
                    "script_raw": script_content
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Task '{task_name}' not found"
                }), 404
                
        except Exception as e:
            app_logger.error(f"Error getting task script: {e}")
            return jsonify({
                "status": "error",
                "message": f"Database error: {str(e)}"
            }), 500

    @app.route('/bulk_update_task_scripts', methods=['POST'], strict_slashes=False)
    def bulk_update_task_scripts():
        """
        Update multiple task scripts in bulk.
        
        Request body:
        {
            "task_scripts": {
                "Review Application": {"action": "validate", "required": true},
                "Approve Contract": {"approval_level": "manager"},
                "Send Notification": {"email_template": "approval_notification"}
            }
        }
        
        PowerShell test:
        $body = @{
            task_scripts = @{
                "Review Application" = @{ action = "validate"; required = $true }
                "Approve Contract" = @{ approval_level = "manager" }
            }
        } | ConvertTo-Json -Depth 3

        Invoke-RestMethod -Uri "http://localhost:5656/bulk_update_task_scripts" -Method POST -Body $body -ContentType "application/json"
        """
        try:
            data = request.get_json()
            
            if not data or 'task_scripts' not in data:
                return jsonify({"status": "error", "message": "task_scripts object is required"}), 400
            
            task_scripts = data['task_scripts']
            results = []
            success_count = 0
            error_count = 0
            
            for task_name, script in task_scripts.items():
                try:
                    # Convert script to JSON string
                    if isinstance(script, dict):
                        script_json = json.dumps(script)
                    else:
                        script_json = str(script) if script is not None else '{}'
                    
                    # Execute stored procedure for each task
                    result = safrs.DB.session.execute(
                        text('EXEC sp_InsertScript @task_name = :task_name, @script = :script'),
                        {"task_name": task_name, "script": script_json}
                    )
                    
                    row = result.fetchone()
                    if row:
                        task_result = {
                            "task_name": task_name,
                            "status": row.Status.lower(),
                            "message": row.Message,
                            "tasks_updated": getattr(row, 'TasksUpdated', 0)
                        }
                        
                        if row.Status.upper() == 'SUCCESS':
                            success_count += 1
                        else:
                            error_count += 1
                    else:
                        task_result = {
                            "task_name": task_name,
                            "status": "error",
                            "message": "No response from stored procedure"
                        }
                        error_count += 1
                    
                    results.append(task_result)
                    
                except Exception as task_error:
                    results.append({
                        "task_name": task_name,
                        "status": "error",
                        "message": str(task_error)
                    })
                    error_count += 1
            
            safrs.DB.session.commit()
            
            return jsonify({
                "status": "completed",
                "total_tasks": len(task_scripts),
                "success_count": success_count,
                "error_count": error_count,
                "results": results
            })
            
        except Exception as e:
            safrs.DB.session.rollback()
            app_logger.error(f"Error in bulk update: {e}")
            return jsonify({
                "status": "error",
                "message": f"Bulk update failed: {str(e)}"
            }), 500