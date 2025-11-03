-- Nested JSON SQL Query for Workflow Hierarchy
-- Returns ProcessDefinitions -> LaneDefinitions -> TaskDefinitions and TaskFlow
-- Compatible with SQL Server JSON functions

WITH WorkflowData AS (
    SELECT 
        pd.ProcessId,
        pd.ProcessName,
        pd.ProcessVersion,
        pd.Description AS ProcessDescription,
        pd.IsActive AS ProcessIsActive,
        pd.CreatedDate AS ProcessCreatedDate,
        pd.CreatedBy AS ProcessCreatedBy,
        pd.ModifiedDate AS ProcessModifiedDate,
        pd.ModifiedBy AS ProcessModifiedBy,
        
        -- Lane Definition data
        ld.LaneId,
        ld.LaneName,
        ld.LaneDescription,
        ld.EstimatedDurationDays,
        ld.LaneRole,
        ld.CreatedDate AS LaneCreatedDate,
        ld.CreatedBy AS LaneCreatedBy,
        ld.ModifiedDate AS LaneModifiedDate,
        ld.ModifiedBy AS LaneModifiedBy,
        
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
        td.PostScriptJson,
        td.CreatedDate AS TaskCreatedDate,
        td.CreatedBy AS TaskCreatedBy,
        td.ModifiedDate AS TaskModifiedDate,
        td.ModifiedBy AS TaskModifiedBy
    FROM ProcessDefinitions pd
    LEFT JOIN LaneDefinitions ld ON pd.ProcessId = ld.ProcessId
    LEFT JOIN TaskDefinitions td ON ld.LaneId = td.LaneId
    WHERE pd.IsActive = 1
),
TaskFlowData AS (
    SELECT 
        tf.FlowId,
        tf.FromTaskId,
        tf.ToTaskId,
        tf.Condition,
        tf.IsDefault,
        
        -- From Task Info
        ft.TaskName AS FromTaskName,
        ft.TaskType AS FromTaskType,
        ft.LaneId AS FromLaneId,
        
        -- To Task Info  
        tt.TaskName AS ToTaskName,
        tt.TaskType AS ToTaskType,
        tt.LaneId AS ToLaneId,
        
        -- Process info for grouping
        ft.ProcessId
    FROM TaskFlow tf
    LEFT JOIN TaskDefinitions ft ON tf.FromTaskId = ft.TaskId
    LEFT JOIN TaskDefinitions tt ON tf.ToTaskId = tt.TaskId
)

SELECT 
    ProcessId,
    ProcessName,
    ProcessVersion,
    ProcessDescription,
    ProcessIsActive,
    ProcessCreatedDate,
    ProcessCreatedBy,
    ProcessModifiedDate,
    ProcessModifiedBy,
    
    -- Nested JSON for Lanes
    (
        SELECT 
            LaneId,
            LaneName,
            LaneDescription,
            EstimatedDurationDays,
            LaneRole,
            LaneCreatedDate,
            LaneCreatedBy,
            LaneModifiedDate,
            LaneModifiedBy,
            
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
                    TaskCreatedDate,
                    TaskCreatedBy,
                    TaskModifiedDate,
                    TaskModifiedBy,
                    
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
        GROUP BY LaneId, LaneName, LaneDescription, EstimatedDurationDays, 
                 LaneRole, LaneCreatedDate, LaneCreatedBy, LaneModifiedDate, LaneModifiedBy
        ORDER BY LaneId
        FOR JSON PATH
    ) AS Lanes,
    
    -- All Task Flows for the entire Process (summary view)
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
         ProcessIsActive, ProcessCreatedDate, ProcessCreatedBy, 
         ProcessModifiedDate, ProcessModifiedBy
         ProcessModifiedDate, ProcessModifiedBy
ORDER BY ProcessId
FOR JSON PATH;

-- Alternative Simpler Version (if the above is too complex)
-- This version creates a flatter structure but still nested

/*
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
WHERE pd.IsActive = 1
ORDER BY pd.ProcessId
FOR JSON PATH;
*/