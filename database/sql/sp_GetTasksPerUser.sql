USE [dashboard]
GO

/****** Object:  StoredProcedure [dbo].[sp_GetTasksPerUser]    Script Date: 10/10/2025 2:45:43 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




CREATE PROCEDURE [dbo].[sp_GetTasksPerUser]
    @username NVARCHAR(255)
  
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validate required parameters
    IF @username IS NULL OR LEN(TRIM(@username)) = 0
    BEGIN
        RAISERROR('Parameter @assignee is required and cannot be empty', 16, 1)
        RETURN
    END

    SELECT  
        ap.[ApplicationID] as applicationId,
        ti.[TaskInstanceId] as taskInstanceId,
        td.[TaskName] as taskName,
        td.[TaskType] as taskType,
        td.[TaskCategory] as TaskCategory,
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
        INNER JOIN roleAssigment ra ON ra.Role = td.AssigneeRole AND ra.Assignee = @username
    WHERE 
        -- Required filters
        ti.status = 'PENDING' AND (td.AssigneeRole != 'SYSTEM')
      
    ORDER BY ap.applicationId, ti.taskInstanceId
END
GO


