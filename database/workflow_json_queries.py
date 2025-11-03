"""
Workflow JSON Query Utilities

Provides functions to execute nested JSON queries for workflow hierarchy data.
Returns ProcessDefinitions -> LaneDefinitions -> TaskDefinitions -> TaskFlow in JSON format.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from sqlalchemy import text
from database.models import ProcessDefinition, LaneDefinition, TaskDefinition, TaskFlow
from database import models
import safrs

app_logger = logging.getLogger("api_logic_server_app")
db = safrs.DB
session = db.session

class WorkflowJSONQuery:
    """
    Utility class for executing workflow hierarchy queries that return nested JSON.
    """
    
    @staticmethod
    def get_workflow_hierarchy_json(process_id: Optional[int] = None, 
                                  include_inactive: bool = False) -> List[Dict[str, Any]]:
        """
        Get complete workflow hierarchy as nested JSON.
        
        Args:
            process_id: Optional process ID to filter by specific process
            include_inactive: Whether to include inactive processes
            
        Returns:
            List of processes with nested lanes, tasks, and flows as JSON
        """
        try:
            # Build the WHERE clause
            where_conditions = []
            if not include_inactive:
                where_conditions.append("pd.IsActive = 1")
            if process_id:
                where_conditions.append(f"pd.ProcessId = {process_id}")
            
            where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            # Main SQL query with nested JSON
            sql_query = f"""
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
                {where_clause}
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
            """
            
            app_logger.info(f"🔍 Executing workflow hierarchy JSON query for process_id={process_id}")
            
            # Execute the query
            result = session.execute(text(sql_query)).fetchall()
            
            # Process results into proper JSON format
            workflow_data = []
            for row in result:
                process_data = {
                    'ProcessId': row.ProcessId,
                    'ProcessName': row.ProcessName,
                    'ProcessVersion': row.ProcessVersion,
                    'ProcessDescription': row.ProcessDescription,
                    'ProcessIsActive': row.ProcessIsActive,
                    'ProcessCreatedDate': row.ProcessCreatedDate.isoformat() if row.ProcessCreatedDate else None,
                    'ProcessCreatedBy': row.ProcessCreatedBy,
                    'Lanes': json.loads(row.Lanes) if row.Lanes else [],
                    'AllTaskFlows': json.loads(row.AllTaskFlows) if row.AllTaskFlows else []
                }
                
                # Parse nested JSON strings in Lanes -> Tasks -> Flows
                for lane in process_data['Lanes']:
                    if 'Tasks' in lane and lane['Tasks']:
                        if isinstance(lane['Tasks'], str):
                            lane['Tasks'] = json.loads(lane['Tasks'])
                        
                        for task in lane['Tasks']:
                            if 'OutgoingFlows' in task and task['OutgoingFlows']:
                                if isinstance(task['OutgoingFlows'], str):
                                    task['OutgoingFlows'] = json.loads(task['OutgoingFlows'])
                            
                            if 'IncomingFlows' in task and task['IncomingFlows']:
                                if isinstance(task['IncomingFlows'], str):
                                    task['IncomingFlows'] = json.loads(task['IncomingFlows'])
                
                workflow_data.append(process_data)
            
            app_logger.info(f"✅ Retrieved {len(workflow_data)} processes with nested hierarchy")
            return workflow_data
            
        except Exception as e:
            app_logger.error(f"❌ Error executing workflow hierarchy query: {str(e)}")
            raise e
    
    @staticmethod
    def get_simple_workflow_json(process_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get simplified workflow hierarchy as nested JSON (easier to parse).
        
        Args:
            process_id: Optional process ID to filter by specific process
            
        Returns:
            List of processes with nested lanes and tasks
        """
        try:
            where_clause = ""
            if process_id:
                where_clause = f"WHERE pd.ProcessId = {process_id} AND pd.IsActive = 1"
            else:
                where_clause = "WHERE pd.IsActive = 1"
            
            # Simplified SQL query
            sql_query = f"""
            SELECT 
                pd.ProcessId,
                pd.ProcessName,
                pd.ProcessVersion,
                pd.Description AS ProcessDescription,
                pd.IsActive AS ProcessIsActive,
                
                -- Lanes as JSON
                (
                    SELECT 
                        ld.LaneId,
                        ld.LaneName,
                        ld.LaneDescription,
                        ld.EstimatedDurationDays,
                        ld.LaneRole,
                        
                        -- Tasks in this lane as JSON
                        (
                            SELECT 
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
                                td.Description AS TaskDescription
                            FROM TaskDefinitions td
                            WHERE td.LaneId = ld.LaneId
                            ORDER BY td.Sequence
                            FOR JSON PATH
                        ) AS Tasks
                        
                    FROM LaneDefinitions ld
                    WHERE ld.ProcessId = pd.ProcessId
                    ORDER BY ld.LaneId
                    FOR JSON PATH
                ) AS Lanes,
                
                -- All TaskFlows for this process
                (
                    SELECT 
                        tf.FlowId,
                        tf.FromTaskId,
                        ft.TaskName AS FromTaskName,
                        tf.ToTaskId,
                        tt.TaskName AS ToTaskName,
                        tf.Condition,
                        tf.IsDefault
                    FROM TaskFlow tf
                    JOIN TaskDefinitions ft ON tf.FromTaskId = ft.TaskId
                    JOIN TaskDefinitions tt ON tf.ToTaskId = tt.TaskId
                    WHERE ft.ProcessId = pd.ProcessId
                    ORDER BY tf.FlowId
                    FOR JSON PATH
                ) AS TaskFlows

            FROM ProcessDefinitions pd
            {where_clause}
            ORDER BY pd.ProcessId
            """
            
            app_logger.info(f"🔍 Executing simple workflow JSON query for process_id={process_id}")
            
            # Execute the query
            result = session.execute(text(sql_query)).fetchall()
            
            # Process results
            workflow_data = []
            for row in result:
                process_data = {
                    'ProcessId': row.ProcessId,
                    'ProcessName': row.ProcessName,
                    'ProcessVersion': row.ProcessVersion,
                    'ProcessDescription': row.ProcessDescription,
                    'ProcessIsActive': row.ProcessIsActive,
                    'Lanes': json.loads(row.Lanes) if row.Lanes else [],
                    'TaskFlows': json.loads(row.TaskFlows) if row.TaskFlows else []
                }
                
                # Parse Tasks JSON in each Lane
                for lane in process_data['Lanes']:
                    if 'Tasks' in lane and lane['Tasks']:
                        if isinstance(lane['Tasks'], str):
                            lane['Tasks'] = json.loads(lane['Tasks'])
                
                workflow_data.append(process_data)
            
            app_logger.info(f"✅ Retrieved {len(workflow_data)} processes with simple hierarchy")
            return workflow_data
            
        except Exception as e:
            app_logger.error(f"❌ Error executing simple workflow query: {str(e)}")
            raise e
    
    @staticmethod
    def get_process_summary_stats() -> Dict[str, Any]:
        """
        Get summary statistics about workflow data.
        
        Returns:
            Dictionary with counts and statistics
        """
        try:
            sql_query = """
            SELECT 
                COUNT(DISTINCT pd.ProcessId) AS TotalProcesses,
                COUNT(DISTINCT ld.LaneId) AS TotalLanes,
                COUNT(DISTINCT td.TaskId) AS TotalTasks,
                COUNT(DISTINCT tf.FlowId) AS TotalFlows,
                COUNT(DISTINCT CASE WHEN pd.IsActive = 1 THEN pd.ProcessId END) AS ActiveProcesses,
                COUNT(DISTINCT CASE WHEN tf.Condition IS NOT NULL AND LEN(TRIM(tf.Condition)) > 0 THEN tf.FlowId END) AS ConditionalFlows,
                AVG(CAST(ld.EstimatedDurationDays AS FLOAT)) AS AvgLaneDurationDays,
                AVG(CAST(td.EstimatedDurationMinutes AS FLOAT)) AS AvgTaskDurationMinutes
            FROM ProcessDefinitions pd
            LEFT JOIN LaneDefinitions ld ON pd.ProcessId = ld.ProcessId
            LEFT JOIN TaskDefinitions td ON ld.LaneId = td.LaneId
            LEFT JOIN TaskFlow tf ON td.TaskId IN (tf.FromTaskId, tf.ToTaskId)
            """
            
            result = session.execute(text(sql_query)).fetchone()
            
            stats = {
                'TotalProcesses': result.TotalProcesses or 0,
                'TotalLanes': result.TotalLanes or 0,
                'TotalTasks': result.TotalTasks or 0,
                'TotalFlows': result.TotalFlows or 0,
                'ActiveProcesses': result.ActiveProcesses or 0,
                'ConditionalFlows': result.ConditionalFlows or 0,
                'AvgLaneDurationDays': round(result.AvgLaneDurationDays or 0, 2),
                'AvgTaskDurationMinutes': round(result.AvgTaskDurationMinutes or 0, 2)
            }
            
            app_logger.info(f"📊 Workflow summary stats: {stats}")
            return stats
            
        except Exception as e:
            app_logger.error(f"❌ Error getting workflow summary stats: {str(e)}")
            return {}

# Utility functions for direct access
def get_workflow_hierarchy_json(process_id: Optional[int] = None, 
                               include_inactive: bool = False) -> List[Dict[str, Any]]:
    """Direct access function for workflow hierarchy JSON."""
    return WorkflowJSONQuery.get_workflow_hierarchy_json(process_id, include_inactive)

def get_simple_workflow_json(process_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Direct access function for simple workflow JSON."""
    return WorkflowJSONQuery.get_simple_workflow_json(process_id)

def get_workflow_summary_stats() -> Dict[str, Any]:
    """Direct access function for workflow summary statistics."""
    return WorkflowJSONQuery.get_process_summary_stats()