"""
Async Application Processing Module
Optimizes get_applications endpoint with concurrent processing
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional
import time

from database.models import WFApplication

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    global _project_dir, _flask_app
    _project_dir = project_dir
    _flask_app = app
    pass

class AsyncApplicationProcessor:
    """
    Async processor for application data with concurrent database operations
    """
    
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_applications_async(self, applications: List, session) -> List[Dict]:
        """
        Process applications concurrently using asyncio
        
        Args:
            applications: List of WFApplication objects
            session: Database session
            
        Returns:
            List of processed application dictionaries
        """
        start_time = time.time()
        app_logger.info(f"🚀 Starting async processing of {len(applications)} applications")
        
        # Create tasks for concurrent processing
        tasks = []
        for app in applications:
            task = asyncio.create_task(
                self._process_single_application_async(app, session)
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out failed applications and log errors
        successful_results = []
        failed_count = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                app_logger.error(f"❌ Failed to process application {applications[i].ApplicationID}: {result}")
                failed_count += 1
            elif result is not None:
                successful_results.append(result)
        
        processing_time = time.time() - start_time
        app_logger.info(f"✅ Async processing completed in {processing_time:.2f}s")
        app_logger.info(f"📊 Success: {len(successful_results)}, Failed: {failed_count}")
        
        return successful_results

    async def _process_single_application_async(self, app: WFApplication, session) -> Optional[Dict]:
        """
        Process a single application asynchronously
        """
        loop = asyncio.get_event_loop()
        
        try:
            # Import Flask context for thread safety
            from flask import current_app
            
            # Get the current app context for the thread
            app_context = current_app._get_current_object()
            
            # Run the database-heavy processing in thread pool with Flask context
            result = await loop.run_in_executor(
                self.executor,
                self._process_application_with_context,
                app, 
                session,
                app_context
            )
            return result
            
        except Exception as e:
            app_logger.error(f"Error processing application {app.ApplicationID}: {e}")
            return None
    
    def _process_application_with_context(self, app, session, flask_app):
        """
        Process application within Flask app context
        """
        with flask_app.app_context():
            return self._process_application_sync(app, session)
    
    def _process_application_sync(self, app, session) -> Dict:
        """
        Synchronous processing of single application (runs in thread pool)
        Optimized with bulk queries and minimal database round trips
        """
        from database.models import (
            CompanyApplication, ProcessInstance, WFFile, WFApplicationMessage, 
            StageInstance, TaskInstance, RoleAssigment, LaneDefinition
        )
        
        app_dict = app.to_dict()
        application_id = app_dict.get("ApplicationID")
        
        if not application_id:
            return None
        
        # Fetch all related data with error handling for bind issues
        try:
            company_app = session.query(CompanyApplication).filter_by(ID=app_dict.get("ApplicationNumber")).first()
        except Exception as e:
            app_logger.error(f"Failed to fetch CompanyApplication for {application_id}: {e}")
            # Create a minimal fallback response
            return {
                "id": application_id,
                "company": "Unknown Company",
                "plant": "Unknown Plant",
                "applicationId": application_id,
                "status": self._get_app_status(app_dict.get("Status", "Unknown")),
                "priority": app_dict.get("Priority", "Normal"),
                "daysInStage": 0,
                "overdue": False,
                "lastUpdate": app_dict.get("ModifiedDate"),
                "documents": 0,
                "notes": 0,
                "assignedRC": "Unassigned",
                "assignedRoles": [],
                "stages": {},
                "application_messages": [],
                "files": [],
                "aiSuggestions": {},
                "plantHistory": {},
                "relatedTasks": {},
                "error": "Database bind error - using fallback data"
            }
        
        if not company_app:
            app_logger.warning(f"Legacy Application source not found for application id {application_id}")
            return None
        
        # Batch fetch related data to minimize queries
        process_instance = session.query(ProcessInstance).filter_by(ApplicationId=application_id).first()
        files = session.query(WFFile).filter_by(ApplicationID=application_id).all()
        app_messages = session.query(WFApplicationMessage).filter_by(ApplicationID=application_id).all()
        assigned_roles = session.query(RoleAssigment).filter_by(ApplicationId=application_id).all()
        
        if not process_instance:
            app_logger.warning(f"Process instance not found for application id {application_id}")
            return None
        
        # Build application data
        app_source = company_app.to_dict()
        created_date = app_dict.get("CreatedDate")
        modified_date = app_dict.get("ModifiedDate")
        status = self._get_app_status(app_dict.get("Status"))
        days_between = self._calc_days_between(created_date, None) if status not in ["COMPL","WTH"] else 0
        days_due = 5  # Fixed due days for overall application
        app_row = {
            "id": application_id,
            "company": app_source.get("CompanyName"),
            "plant": app_source.get("PlantName"),
            #"plantHistory": {},
            "applicationId": application_id,
            "region": app_source.get("Region"),
            "priority": app_dict.get("Priority", "Normal"),
            "status": status,
            "assignedRC": app_source.get("AssignedTo"),
            "daysInProcess": days_between,
            "daysOverdue": days_between - days_due if days_between > days_due and status != "COMPL" else 0,
            "isOverdue": days_between > days_due if status != "COMPL" else False,
            #"nextAction": "Follow up on contract",
            "documents": len(files) if files else 0,
            "createdDate": created_date,
            "lastUpdate": modified_date,
            "notes": len(app_messages) if app_messages else 0,
            #"aiSuggestions": {},
            #"assignedRC": app_source.get("AssignedTo", "Unassigned"),
            "assignedRoles": [{ role.WF_Role.UserRole: role.Assignee} for role in assigned_roles]
        }
        
        # Process stages and tasks efficiently
        app_row["stages"] = self._process_stages_optimized(process_instance, session)
        
        # Process messages
        app_row["application_messages"] = []
        for am in app_messages:
            msg = am.to_dict()
            app_row["application_messages"].append({
                "id": msg.get("MessageID"),
                "fromUser": msg.get("FromUser"), 
                "toUser": msg.get("ToUser"),
                "priority": msg.get("Priority"),
                "text": msg.get("MessageText"),
                "sentDate": msg.get("SentDate"),
                "messageType": msg.get("MessageType"),
            })
        
        app_row['files'] = []
        app_row["aiSuggestions"] = {}
        app_row["plantHistory"] = {}
        app_row["relatedTasks"] = {}
        
        return app_row
    
    def _process_stages_optimized(self, process_instance, session) -> Dict:
        """
        Process stages with optimized queries
        """
        from database.models import StageInstance, TaskInstance, LaneDefinition
        
        # Fetch all stages for this process instance
        stages = session.query(StageInstance).filter_by(
            ProcessInstanceId=process_instance.InstanceId
        ).order_by(StageInstance.StageInstanceId).all()
        
        if not stages:
            return {}
        
        # Fetch all tasks for all stages in one query
        stage_ids = [stage.StageInstanceId for stage in stages]
        all_tasks = session.query(TaskInstance).filter(
            TaskInstance.StageId.in_(stage_ids)
        ).order_by(TaskInstance.TaskInstanceId).all()
        
        # Fetch all lanes in one query
        lane_ids = [stage.LaneId for stage in stages]
        lanes = session.query(LaneDefinition).filter(
            LaneDefinition.LaneId.in_(lane_ids)
        ).all()
        lane_dict = {lane.LaneId: lane for lane in lanes}
        
        # Group tasks by stage
        tasks_by_stage = {}
        for task in all_tasks:
            if task.StageId not in tasks_by_stage:
                tasks_by_stage[task.StageId] = []
            tasks_by_stage[task.StageId].append(task)
        
        result_stages = {}
        
        for stage in stages:
            stage_dict = stage.to_dict()
            stage_tasks = tasks_by_stage.get(stage.StageInstanceId, [])
            
            tasks = []
            task_cnt = 0
            completed_cnt = 0
            
            for task in stage_tasks:
                if (task.TaskDef and task.TaskDef.AutoComplete == True or 
                    task.TaskDef and task.TaskDef.TaskType in ['START','END',"LANESTART",'LANEEND']):
                    continue
                
                task_cnt += 1
                completed_cnt += 1 if task.Status == 'COMPLETED' else 0
                
                created_date = task.StartedDate
                modified_date = datetime.now() if task.Status != 'COMPLETED' else task.CompletedDate
                days_between = self._calc_days_between(created_date, modified_date)
                days_due = int(task.TaskDef.EstimatedDurationMinutes / 60 * 24) if task.TaskDef and task.TaskDef.EstimatedDurationMinutes else 1
                tasks.append({
                    "name": task.TaskDef.TaskName if task and task.TaskDef else "Unknown Task Name",
                    "status": task.Status,
                    "taskType": task.TaskDef.TaskType if task and task.TaskDef else "Unknown Task Type",
                    "taskCategory": task.TaskDef.TaskCategory if task and task.TaskDef else "Unknown Task Category",
                    "executedBy": task.AssignedTo,
                    "daysPending": days_between,
                    "daysOverdue": days_between - days_due if days_between > days_due and task.Status != 'COMPLETED' else 0,
                    "isOverdue": days_between > days_due and task.Status != 'COMPLETED',
                    "createdDate": task.StartedDate,
                    "description": task.TaskDef.Description if task and task.TaskDef else " ",
                    "required": task.TaskDef.IsRequired if task and task.TaskDef else False,
                    "TaskInstanceId": task.TaskInstanceId,
                    "PreScript": self._get_pre_script(task),
                    "CompletedDate": task.CompletedDate,
                    "Result": task.Result,
                    "ResultData": task.ResultData,
                    "ErrorMessage": task.ErrorMessage,
                    "taskRoles": [{
                        "taskRole": task.TaskDef.AssigneeRole if task and task.TaskDef else "Unknown Role"
                    }],
                })
            
            lane = lane_dict.get(stage_dict['LaneId'])
            if lane:
                lane_dict_data = lane.to_dict()
                lane_name = lane_dict_data["LaneName"]
                result_stages[lane_name] = {
                    "status": stage_dict["Status"], 
                    "description": lane_dict_data["LaneDescription"],
                    "progress": int(completed_cnt / task_cnt * 100) if task_cnt > 0 and completed_cnt > 0 else 0,
                    "tasks": tasks
                }
        
        return result_stages
    
    def _get_pre_script(self, task) -> str:
        """Get pre-script for task"""
        default_script = '''
            {
                "Title": "{{ Title }}",
                "Description": "{{ Description }}",
                "ApplicationID": "{{ ApplicationID }}",
                "TaskInstanceId": "{{ TaskInstanceId }}"
            }
        '''
        
        script = task.TaskDef.PreScriptJson if task and task.TaskDef and task.TaskDef.PreScriptJson else {}
        
        if script and isinstance(script, str) and '{{' in script:
            from jinja2 import Template
            template = Template(script)
            title = task.TaskDef.TaskName if task and task.TaskDef else "Unknown Task Name"
            description = task.TaskDef.Description if task and task.TaskDef else " "
            application_id = task.Stage.ProcessInstance.ApplicationId if task and task.Stage and task.Stage.ProcessInstance else None
            task_id = task.TaskInstanceId if task else None
            script = template.render(
                Title=title, 
                Description=description, 
                ApplicationID=application_id, 
                TaskInstanceId=task_id
            )
        
        return script
    
    def _calc_days_between(self, start_date, end_date) -> int:
        """Calculate days between two dates"""
        if not end_date:
            end_date = datetime.fromisoformat(datetime.now().isoformat()).isoformat()
        if start_date and end_date:
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            return (end_date - start_date).days
        return 0
    
    def _get_app_status(self, status_code: str) -> str:
        """Get application status from code"""
        status_map = {
            "NEW": "New",
            "INP": "In Progress",
            "HLD": "On Hold",
            "WTH": "Withdrawn",
            "COMPL": "Certified",
            "REJ": "Rejected",
            "REVIEW": "Inspection Report Submitted to IAR",
            "INSPECTION": "Inspection Scheduled",
            "PAYPEND": "Payment Pending",
            "CONTRACT": "Contract Sent to Customer"
        }
        return status_map.get(status_code, "Unknown Status")


# Global processor instance
async_processor = AsyncApplicationProcessor(max_workers=10)


async def process_applications_concurrently(applications: List, session, max_workers: int = 10) -> List[Dict]:
    """
    Convenience function to process applications concurrently
    
    Args:
        applications: List of WFApplication objects
        session: Database session
        max_workers: Maximum number of concurrent workers
        
    Returns:
        List of processed application dictionaries
    """
    processor = AsyncApplicationProcessor(max_workers=max_workers)
    return await processor.process_applications_async(applications, session)
