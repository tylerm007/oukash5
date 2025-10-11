"""
Python wrapper functions for sp_InsertScript stored procedure
"""

import logging
from sqlalchemy import text
from typing import Dict, Any, Optional
import json

app_logger = logging.getLogger(__name__)

def insert_task_script(session, task_name: str, script: str) -> Dict[str, Any]:
    """
    Insert or update PostScriptJson for a task definition using stored procedure.
    
    Args:
        session: SQLAlchemy session
        task_name: Name of the task to update
        script: JSON script content (string or dict)
        
    Returns:
        Dictionary with operation results
    """
    try:
        # Convert dict to JSON string if needed
        if isinstance(script, dict):
            script = json.dumps(script)
        elif script is None:
            script = '{}'
            
        app_logger.info(f"Updating script for task: {task_name}")
        
        # Execute stored procedure
        result = session.execute(
            text('EXEC sp_InsertScript @task_name = :task_name, @script = :script'),
            {"task_name": task_name, "script": script}
        )
        
        # Get the result row
        row = result.fetchone()
        if row:
            response = {
                "status": row.Status,
                "message": row.Message,
                "task_name": row.TaskName,
                "tasks_found": getattr(row, 'TasksFound', 0),
                "tasks_updated": getattr(row, 'TasksUpdated', 0),
                "task_id": getattr(row, 'TaskId', None),
                "updated_script": getattr(row, 'UpdatedScript', script)
            }
        else:
            response = {
                "status": "ERROR",
                "message": "No response from stored procedure",
                "task_name": task_name
            }
            
        session.commit()
        app_logger.info(f"Script update result: {response['status']} - {response['message']}")
        return response
        
    except Exception as e:
        session.rollback()
        error_msg = f"Error updating task script: {str(e)}"
        app_logger.error(error_msg)
        return {
            "status": "ERROR",
            "message": error_msg,
            "task_name": task_name
        }

def bulk_insert_task_scripts(session, task_scripts: Dict[str, str]) -> Dict[str, Any]:
    """
    Update multiple task scripts in bulk.
    
    Args:
        session: SQLAlchemy session
        task_scripts: Dictionary of {task_name: script_content}
        
    Returns:
        Dictionary with bulk operation results
    """
    results = []
    success_count = 0
    error_count = 0
    
    for task_name, script in task_scripts.items():
        result = insert_task_script(session, task_name, script)
        results.append(result)
        
        if result["status"] == "SUCCESS":
            success_count += 1
        else:
            error_count += 1
    
    return {
        "total_tasks": len(task_scripts),
        "success_count": success_count,
        "error_count": error_count,
        "results": results
    }

def get_task_script(session, task_name: str) -> Optional[str]:
    """
    Get the current PostScriptJson for a task.
    
    Args:
        session: SQLAlchemy session
        task_name: Name of the task
        
    Returns:
        JSON script string or None if not found
    """
    try:
        result = session.execute(
            text('SELECT PostScriptJson FROM TaskDefinitions WHERE TaskName = :task_name'),
            {"task_name": task_name}
        )
        row = result.fetchone()
        return row.PostScriptJson if row else None
        
    except Exception as e:
        app_logger.error(f"Error getting task script for {task_name}: {e}")
        return None

# Example usage functions for API endpoints
def example_api_usage():
    """
    Example of how to use these functions in your API endpoints
    """
    # Example 1: Single task update
    script_content = {
        "action": "validate_application",
        "fields": ["company_name", "contact_email"],
        "required": True,
        "auto_proceed": False
    }
    
    result = insert_task_script(session, "Review Application", script_content)
    
    # Example 2: Bulk update
    bulk_scripts = {
        "Review Application": '{"action": "validate", "required": true}',
        "Approve Contract": '{"approval_level": "manager"}',
        "Send Notification": '{"email_template": "approval_notification"}'
    }
    
    bulk_result = bulk_insert_task_scripts(session, bulk_scripts)
    
    # Example 3: Get current script
    current_script = get_task_script(session, "Review Application")
    
    return {
        "single_update": result,
        "bulk_update": bulk_result,
        "current_script": current_script
    }