
-- Stored Procedure: Get Tasks with Parameters
-- Usage: EXEC sp_GetTasksView @assignee = 'user1', @assignee_role = 'ADMIN,USER', @status = 'PENDING'

IF OBJECT_ID('dbo.sp_GetTasksView', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_GetTasksView
GO

CREATE PROCEDURE dbo.sp_GetTasksView
    @assignee NVARCHAR(255),
    @assignee_role NVARCHAR(1000) = NULL,
    @status NVARCHAR(50) = 'PENDING',
    @application_id INT = NULL,
    @company_id INT = NULL,
    @plant_id INT = NULL,
    @lane_name NVARCHAR(255) = NULL,
    @task_type NVARCHAR(50) = NULL,
    @include_system_roles BIT = 0  -- 0 = exclude SYSTEM roles, 1 = include
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate required parameters
    IF @assignee IS NULL OR LEN(TRIM(@assignee)) = 0
    BEGIN
        RAISERROR('Parameter @assignee is required and cannot be empty', 16, 1)
        RETURN
    END
    
    -- Default assignee_role to all roles if not provided
    IF @assignee_role IS NULL OR LEN(TRIM(@assignee_role)) = 0
    BEGIN
        SELECT @assignee_role = STRING_AGG(DISTINCT Role, ',')
        FROM roleAssigment 
        WHERE Assignee = @assignee
    END
    
    SELECT  
        ti.[TaskInstanceId] as taskInstanceId,
        ap.[ApplicationID] as applicationId,
        td.[TaskName] as taskName,
        td.[TaskType] as taskType,
        td.[AssigneeRole] as assigneeRole,
        ra.Assignee as assignee,
        ap.CompanyId as companyId,
        ap.PlantID as plantId,
        co.NAME as companyName,
        pl.NAME as plantName,
        ld.LaneName as laneName,
        ti.[Status] as status,
        ti.[StartedDate] as startedDate,
        ti.[CompletedDate] as completedDate,
        ti.[CreatedDate] as createdDate,
        ti.[CreatedBy] as createdBy,
        pi.InstanceId as processInstanceId,
        si.StageInstanceId as stageInstanceId
    FROM [dashboard].[dbo].[TaskInstances] ti
        INNER JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
        INNER JOIN StageInstance si ON ti.StageId = si.StageInstanceId
        INNER JOIN ProcessInstances pi ON si.ProcessInstanceId = pi.InstanceId
        INNER JOIN WF_Applications ap ON pi.ApplicationId = ap.ApplicationID
        INNER JOIN LaneDefinitions ld ON si.LaneId = ld.LaneId
        LEFT JOIN ou_kash.dbo.plant_tb pl ON ap.plantID = pl.plant_ID
        LEFT JOIN ou_kash.dbo.COMPANY_TB co ON ap.companyId = co.COMPANY_ID
        INNER JOIN roleAssigment ra ON ra.Role = td.AssigneeRole AND ra.Assignee = @assignee
    WHERE 
        -- Required filters
        ti.status = @status
        AND (@include_system_roles = 1 OR td.AssigneeRole != 'SYSTEM')
        AND td.AssigneeRole IN (SELECT TRIM(value) FROM STRING_SPLIT(@assignee_role, ','))
        
        -- Optional filters
        AND (@application_id IS NULL OR ap.ApplicationID = @application_id)
        AND (@company_id IS NULL OR ap.CompanyId = @company_id)
        AND (@plant_id IS NULL OR ap.PlantID = @plant_id)
        AND (@lane_name IS NULL OR ld.LaneName = @lane_name)
        AND (@task_type IS NULL OR td.TaskType = @task_type)
    
    ORDER BY ap.applicationId, ti.taskInstanceId
END
GO

-- Grant permissions (adjust as needed)
-- GRANT EXECUTE ON dbo.sp_GetTasksView TO [your_app_user]
GO

-- Example usage:
/*
-- Basic usage
EXEC sp_GetTasksView @assignee = 'user1', @assignee_role = 'ADMIN,USER'

-- With optional filters
EXEC sp_GetTasksView 
    @assignee = 'user1',
    @assignee_role = 'ADMIN,USER',
    @status = 'PENDING',
    @application_id = 123,
    @company_id = 456

-- Include system roles
EXEC sp_GetTasksView 
    @assignee = 'admin',
    @assignee_role = '('DISPATCHER','NCRC','LEGAL')',
    @include_system_roles = 1
*/