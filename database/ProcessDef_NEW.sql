use dashboard;
-- =============================================
-- Admin Completion Workflow - SQL Server DDL
-- BPMN-based Workflow Management System
-- =============================================

-- =============================================
-- Core Workflow Tables
-- =============================================
-- =============================================
-- Drop Tables (Child Tables First)
-- =============================================

-- Drop views first
IF OBJECT_ID('vw_ActiveWorkflows', 'V') IS NOT NULL DROP VIEW vw_ActiveWorkflows;
IF OBJECT_ID('vw_ValidationStatus', 'V') IS NOT NULL DROP VIEW vw_ValidationStatus;
IF OBJECT_ID('vw_TaskPerformance', 'V') IS NOT NULL DROP VIEW vw_TaskPerformance;
IF OBJECT_ID('vw_WorkflowDashboard', 'V') IS NOT NULL DROP VIEW vw_WorkflowDashboard;
IF OBJECT_ID('vw_BottleneckAnalysis', 'V') IS NOT NULL DROP VIEW vw_BottleneckAnalysis;

-- Drop triggers
IF OBJECT_ID('tr_TaskCompletion_AutoAdvance', 'TR') IS NOT NULL DROP TRIGGER tr_TaskCompletion_AutoAdvance;

-- Drop functions
IF OBJECT_ID('fn_AllValidationsPassed', 'FN') IS NOT NULL DROP FUNCTION fn_AllValidationsPassed;

-- Drop stored procedures
IF OBJECT_ID('sp_StartWorkflowInstance', 'P') IS NOT NULL DROP PROCEDURE sp_StartWorkflowInstance;
IF OBJECT_ID('sp_CompleteTask', 'P') IS NOT NULL DROP PROCEDURE sp_CompleteTask;
IF OBJECT_ID('sp_RunValidationCheck', 'P') IS NOT NULL DROP PROCEDURE sp_RunValidationCheck;
IF OBJECT_ID('sp_AddMessage', 'P') IS NOT NULL DROP PROCEDURE IF EXISTS sp_AddMessage;
IF OBJECT_ID('sp_AddComment', 'P') IS NOT NULL DROP PROCEDURE sp_AddComment;
IF OBJECT_ID('sp_GetWorkflowStatus', 'P') IS NOT NULL DROP PROCEDURE sp_GetWorkflowStatus;

-- Truncate child tables first (tables with foreign keys)
IF OBJECT_ID('WorkflowHistory', 'U') IS NOT NULL DELETE FROM WorkflowHistory;
IF OBJECT_ID('TaskComments', 'U') IS NOT NULL DELETE FROM TaskComments;
IF OBJECT_ID('ProcessMessages', 'U') IS NOT NULL DELETE FROM ProcessMessages;
IF OBJECT_ID('ValidationResults', 'U') IS NOT NULL DELETE FROM ValidationResults;
IF OBJECT_ID('StageInstance', 'U') IS NOT NULL DELETE FROM StageInstance;
IF OBJECT_ID('TaskInstances', 'U') IS NOT NULL DELETE FROM TaskInstances;
IF OBJECT_ID('TaskStatus','U') IS NOT NULL DELETE FROM TaskStatus;
IF OBJECT_ID('ProcessInstances', 'U') IS NOT NULL DELETE FROM ProcessInstances;
IF OBJECT_ID('TaskFlow', 'U') IS NOT NULL DELETE FROM TaskFlow;
IF OBJECT_ID('TaskDefinitions', 'U') IS NOT NULL DELETE FROM TaskDefinitions;
IF OBJECT_ID('ProcessDefinitions', 'U') IS NOT NULL DELETE FROM ProcessDefinitions;
IF OBJECT_ID('TaskCategories', 'U') IS NOT NULL DELETE FROM TaskCategories;
IF OBJECT_ID('TaskTypes', 'U') IS NOT NULL DELETE FROM TaskTypes;
IF OBJECT_ID('LaneDefinitions', 'U') IS NOT NULL DELETE FROM LaneDefinitions;

-- Drop child tables first (tables with foreign keys)
IF OBJECT_ID('WorkflowHistory', 'U') IS NOT NULL DROP TABLE WorkflowHistory;
IF OBJECT_ID('TaskComments', 'U') IS NOT NULL DROP TABLE TaskComments;
IF OBJECT_ID('ProcessMessages', 'U') IS NOT NULL DROP TABLE ProcessMessages;
IF OBJECT_ID('ValidationResults', 'U') IS NOT NULL DROP TABLE ValidationResults;
IF OBJECT_ID('StageInstance', 'U') IS NOT NULL DROP TABLE StageInstance;
IF OBJECT_ID('TaskInstances', 'U') IS NOT NULL DROP TABLE TaskInstances;
IF OBJECT_ID('TaskStatus','U') IS NOT NULL DROP TABLE TaskStatus;
IF OBJECT_ID('ProcessInstances', 'U') IS NOT NULL DROP TABLE ProcessInstances;
IF OBJECT_ID('TaskFlow', 'U') IS NOT NULL DROP TABLE TaskFlow;
IF OBJECT_ID('TaskDefinitions', 'U') IS NOT NULL DROP TABLE TaskDefinitions;
IF OBJECT_ID('TaskCategories', 'U') IS NOT NULL DROP TABLE TaskCategories;
IF OBJECT_ID('TaskTypes', 'U') IS NOT NULL DROP TABLE TaskTypes;
IF OBJECT_ID('LaneDefinitions', 'U') IS NOT NULL DROP TABLE LaneDefinitions;

-- Drop parent tables (tables with primary keys referenced by others)
IF OBJECT_ID('LaneRoles', 'U') IS NOT NULL DROP TABLE LaneRoles;
IF OBJECT_ID('StageStatus', 'U') IS NOT NULL DROP TABLE StageStatus;
IF OBJECT_ID('TaskCommentTypes', 'U') IS NOT NULL DROP TABLE TaskCommentTypes;
IF OBJECT_ID('ProcessMessageTypes', 'U') IS NOT NULL DROP TABLE ProcessMessageTypes;
IF OBJECT_ID('ValidationRules', 'U') IS NOT NULL DROP TABLE ValidationRules;
IF OBJECT_ID('ProcessDefinitions', 'U') IS NOT NULL DROP TABLE ProcessDefinitions;
IF OBJECT_ID('ProcessStatus', 'U') IS NOT NULL DROP TABLE ProcessStatus;
IF OBJECT_ID('ProcessPriorities', 'U') IS NOT NULL DROP TABLE IF EXISTS ProcessPriorities;

PRINT 'All tables, views, procedures, functions, and triggers dropped successfully.';
-- Workflow Process Definitions
CREATE TABLE ProcessDefinitions (
    ProcessId INT IDENTITY(1,1) PRIMARY KEY,
    ProcessName NVARCHAR(100) NOT NULL,
    ProcessVersion NVARCHAR(10) NOT NULL DEFAULT '1.0',
    Description NVARCHAR(500),
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy NVARCHAR(100) NOT NULL,
    ModifiedDate DATETIME2,
    ModifiedBy NVARCHAR(100)
);

-- Lookup table for Lane Roles
CREATE TABLE LaneRoles (
    RoleCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    RoleDescription NVARCHAR(255) NOT NULL
);


CREATE TABLE LaneDefinitions(
	LaneId INT IDENTITY(1,1) PRIMARY KEY,
	ProcessId INT NOT NULL,
	LaneName nvarchar(100) NOT NULL,
	LaneDescription nvarchar(500) NULL,
	EstimatedDurationDays int NULL,
    LaneRole NVARCHAR(20) NOT NULL DEFAULT 'NCRC', -- NCRC, Sales, Legal, Finance, Ingredients, Products
	CreatedDate datetime2(7) NOT NULL DEFAULT GETUTCDATE(),
	CreatedBy nvarchar(100) NOT NULL,
    ModifiedDate datetime2(7) NULL,
    ModifiedBy nvarchar(100) NULL,
    FOREIGN KEY (LaneRole) REFERENCES LaneRoles(RoleCode),
    FOREIGN KEY (ProcessId) REFERENCES ProcessDefinitions(ProcessId)
);

CREATE TABLE TaskTypes (
    TaskTypeCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    TaskTypeDescription NVARCHAR(255) NOT NULL
);


CREATE TABLE TaskCategories (
    TaskCategoryCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    TaskCategoryDescription NVARCHAR(255) NOT NULL
);  

-- Task Definitions within Processes
CREATE TABLE TaskDefinitions (
    TaskId INT IDENTITY(1,1) PRIMARY KEY,
    ProcessId INT NOT NULL,
    TaskName NVARCHAR(100) NOT NULL,
    TaskType NVARCHAR(20) NOT NULL, -- 'UserTask', 'ServiceTask', 'ScriptTask', 'Gateway', 'Event'
    TaskCategory NVARCHAR(20), -- 'Validation', 'Action', 'Decision', 'Notification'
    Sequence INT NOT NULL,
    LaneId INT NOT NULL,
    IsParallel BIT NOT NULL DEFAULT 0,
    AssigneeRole NVARCHAR(20), -- Inherited role for process definition 
    EstimatedDurationMinutes INT,
    IsRequired BIT NOT NULL DEFAULT 1,
    AutoComplete BIT NOT NULL DEFAULT 0,
    Description NVARCHAR(500),
    ConfigurationJson NVARCHAR(MAX), -- JSON configuration for task-specific settings
    FOREIGN KEY (TaskCategory) REFERENCES TaskCategories(TaskCategoryCode),
    FOREIGN KEY (TaskType) REFERENCES TaskTypes(TaskTypeCode),
    FOREIGN KEY (LaneId) REFERENCES LaneDefinitions(LaneId),
    FOREIGN KEY (ProcessId) REFERENCES ProcessDefinitions(ProcessId)
);

-- Task Dependencies and Flow
CREATE TABLE TaskFlow (
    FlowId INT IDENTITY(1,1) PRIMARY KEY,
    FromTaskId INT,
    ToTaskId INT NOT NULL,
    Condition NVARCHAR(500), -- Conditional logic for flow
    IsDefault BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (FromTaskId) REFERENCES TaskDefinitions(TaskId),
    FOREIGN KEY (ToTaskId) REFERENCES TaskDefinitions(TaskId)
);

-- =============================================
-- Workflow Instance Tables
-- =============================================
CREATE TABLE ProcessStatus (
    StatusCode NVARCHAR(10) NOT NULL PRIMARY KEY,   
    StatusDescription NVARCHAR(255) NOT NULL
);


CREATE TABLE ProcessPriorities (
    PriorityCode NVARCHAR(10) NOT NULL PRIMARY KEY,
    PriorityDescription NVARCHAR(255) NOT NULL
);  


-- Application Workflow Instances
CREATE TABLE ProcessInstances (
    InstanceId INT IDENTITY(1,1) PRIMARY KEY,
    ProcessId INT NOT NULL,
    ApplicationId INT NOT NULL, -- wf_application reference
    Status NVARCHAR(10) NOT NULL DEFAULT 'NEW', -- 'Active', 'Completed', 'Suspended', 'Terminated'
    CurrentTaskId INT, -- ? NOT SURE HOW TO MAKE THIS WORK
    StartedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    StartedBy NVARCHAR(100) NOT NULL,
    CompletedDate DATETIME2,
    CompletedBy NVARCHAR(100),
    Priority NVARCHAR(10) DEFAULT 'NORMAL', -- 'Low', 'Normal', 'High', 'Critical' ProcessPriorities FK
    ContextData NVARCHAR(MAX), -- JSON data for workflow context
    FOREIGN KEY (Priority) REFERENCES ProcessPriorities(PriorityCode),
    FOREIGN KEY (Status) REFERENCES ProcessStatus(StatusCode),
    FOREIGN KEY (ProcessId) REFERENCES ProcessDefinitions(ProcessId),
    FOREIGN KEY (CurrentTaskId) REFERENCES TaskDefinitions(TaskId)
);

-- Stage Status Lookup Table
CREATE TABLE StageStatus (
    StatusCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    StatusDescription NVARCHAR(255) NOT NULL
);

-- Stage Instance is a specific instance of a stage within a process
CREATE TABLE StageInstance(
    StageInstanceId INT IDENTITY(1,1) PRIMARY KEY,
    ProcessInstanceId INT NOT NULL,
    LaneId INT NOT NULL, -- link back to LaneDefinitions
    Status nvarchar(20) NOT NULL DEFAULT 'NEW',
    StartedDate datetime2(7) NULL,
    CompletedDate datetime2(7) NULL, -- RULE.formula when Status == Completed return current_date
    DurationDays  AS (datediff(day,StartedDate,CompletedDate)),
    RetryCount int NULL,
    AssignedTo nvarchar(100) NULL, -- User email
    AssignedBy nvarchar(100) NULL, -- User email
    AssignedDate datetime2(7) NULL, -- Rule.formula when AssignedTo is not null return current_date
    CompletedCount int NULL, -- Rule to Count Completed Tasks
    TotalCount int NULL, -- Rule to Count Total Tasks
    CreatedDate datetime2(7) NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy nvarchar(100) NOT NULL DEFAULT 'System',
    ModifiedDate datetime2(7) NULL,
    ModifiedBy nvarchar(100) NULL,
    FOREIGN KEY (ProcessInstanceId) REFERENCES ProcessInstances(InstanceId),
    FOREIGN KEY (LaneId) REFERENCES LaneDefinitions(LaneId),
    FOREIGN KEY (Status) REFERENCES StageStatus(StatusCode)
);

-- Task Status Lookup Table
CREATE TABLE TaskStatus (
    StatusCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    StatusDescription NVARCHAR(255) NOT NULL
);

-- Task Status
INSERT INTO TaskStatus (StatusCode, StatusDescription) VALUES
('Pending', 'Task Pending Execution'),
('Running', 'Task Currently Running'),
('Completed', 'Task Completed Successfully'),
('Failed', 'Task Failed'),
('Skipped', 'Task Skipped'),
('Cancelled', 'Task Cancelled');

-- Task Instance Execution
CREATE TABLE TaskInstances (
    TaskInstanceId INT IDENTITY(1,1) PRIMARY KEY,
    TaskId INT NOT NULL, -- TaskDefinition
    StageId INT NOT NULL, -- StageInstance
    Status NVARCHAR(20) NOT NULL DEFAULT 'Pending', -- 'Pending', 'InProgress', 'Completed', 'Failed', 'Skipped'
    AssignedTo NVARCHAR(100),
    StartedDate DATETIME2,
    CompletedDate DATETIME2,
    DurationMinutes AS DATEDIFF(MINUTE, StartedDate, CompletedDate),
    Result NVARCHAR(50), -- 'Success', 'Failed', 'Retry', 'Skip'
    ResultData NVARCHAR(MAX), -- JSON result data
    ErrorMessage NVARCHAR(1000),
    RetryCount INT DEFAULT 0,
    FOREIGN KEY (Status) REFERENCES TaskStatus(StatusCode),
    FOREIGN KEY (StageId) REFERENCES StageInstances(StageInstanceId),
    FOREIGN KEY (TaskId) REFERENCES TaskDefinitions(TaskId)
);

-- =============================================
-- Validation Framework Tables
-- =============================================

-- Validation Rules
CREATE TABLE ValidationRules (
    ValidationId INT IDENTITY(1,1) PRIMARY KEY,
    ValidationName NVARCHAR(100) NOT NULL,
    Category NVARCHAR(50) NOT NULL, -- 'Company', 'Plant', 'Contacts', 'Products', 'Ingredients', 'Quote', 'Documentation'
    RuleType NVARCHAR(50) NOT NULL, -- 'Required', 'Format', 'Business', 'CrossReference'
    ValidationQuery NVARCHAR(MAX), -- SQL query for validation
    ErrorMessage NVARCHAR(500),
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

-- Validation Results
CREATE TABLE ValidationResults (
    ValidationResultId INT IDENTITY(1,1) PRIMARY KEY,
    InstanceId INT NOT NULL,
    ValidationId INT NOT NULL,
    TaskInstanceId INT,
    IsValid BIT NOT NULL,
    ValidationMessage NVARCHAR(500),
    ValidationDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ValidatedBy NVARCHAR(100),
    FOREIGN KEY (InstanceId) REFERENCES ProcessInstances(InstanceId),
    FOREIGN KEY (ValidationId) REFERENCES ValidationRules(ValidationId),
    FOREIGN KEY (TaskInstanceId) REFERENCES TaskInstances(TaskInstanceId)
);

-- =============================================
-- Communication Tables
-- =============================================
-- Message Types Lookup Table
CREATE TABLE ProcessMessageTypes (
    MessageTypeCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    MessageTypeDescription NVARCHAR(255) NOT NULL
);

INSERT INTO ProcessMessageTypes (MessageTypeCode, MessageTypeDescription) VALUES
    ('Standard', 'Standard message'),
    ('Urgent', 'Urgent message requiring immediate attention'),
    ('System', 'System-generated message'),
    ('Notification', 'Notification message');

-- ProcessMessages
CREATE TABLE ProcessMessages (
    MessageId INT IDENTITY(1,1) PRIMARY KEY,
    InstanceId INT NOT NULL,
    FromUser NVARCHAR(100) NOT NULL,
    ToUser NVARCHAR(100),
    ToRole NVARCHAR(50),
    MessageType NVARCHAR(20) DEFAULT 'Standard', -- 'Standard', 'Urgent', 'System', 'Notification'
    Subject NVARCHAR(200),
    MessageBody NVARCHAR(MAX) NOT NULL,
    SentDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ReadDate DATETIME2,
    IsRead BIT NOT NULL DEFAULT 0,
    FOREIGN KEY (MessageType) REFERENCES ProcessMessageTypes(MessageTypeCode),
    FOREIGN KEY (InstanceId) REFERENCES ProcessInstances(InstanceId)
);

-- Comment Types Lookup Table
CREATE TABLE TaskCommentTypes (
    CommentTypeCode NVARCHAR(10) NOT NULL PRIMARY KEY,
    CommentTypeDescription NVARCHAR(255) NOT NULL
);

INSERT INTO TaskCommentTypes (CommentTypeCode, CommentTypeDescription) VALUES
    ('Internal', 'Internal comment for staff use only'),
    ('External', 'External comment visible to clients'),
    ('System', 'System-generated comment');

-- TaskComments
CREATE TABLE TaskComments (
    CommentId INT IDENTITY(1,1) PRIMARY KEY,
    ProcessInstanceId INT NOT NULL,
    TaskInstanceId INT,
    CommentType NVARCHAR(10) DEFAULT 'Internal', -- 'Internal', 'External', 'System'
    CommentText NVARCHAR(MAX) NOT NULL,
    Author NVARCHAR(100) NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    IsVisible BIT NOT NULL DEFAULT 1,
    FOREIGN KEY (CommentType) REFERENCES TaskCommentTypes(CommentTypeCode),
    FOREIGN KEY (ProcessInstanceId) REFERENCES ProcessInstance(InstanceId),
    FOREIGN KEY (TaskInstanceId) REFERENCES TaskInstances(TaskInstanceId)
);

-- =============================================
-- Audit and History Tables
-- =============================================

-- Workflow History
CREATE TABLE WorkflowHistory (
    HistoryId INT IDENTITY(1,1) PRIMARY KEY,
    InstanceId INT NOT NULL,
    TaskInstanceId INT,
    Action NVARCHAR(100) NOT NULL,
    PreviousStatus NVARCHAR(50),
    NewStatus NVARCHAR(50),
    ActionBy NVARCHAR(100) NOT NULL,
    ActionDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ActionReason NVARCHAR(500),
    Details NVARCHAR(MAX), -- JSON details
    FOREIGN KEY (InstanceId) REFERENCES ProcessInstances(InstanceId),
    FOREIGN KEY (TaskInstanceId) REFERENCES TaskInstances(TaskInstanceId)
);

-- =============================================
-- Indexes for Performance
-- =============================================

CREATE INDEX IX_ProcessInstances_ApplicationId ON ProcessInstances(ApplicationId);
CREATE INDEX IX_ProcessInstances_Status ON ProcessInstances(Status);
CREATE INDEX IX_ProcessInstances_StartedDate ON ProcessInstances(StartedDate);

CREATE INDEX IX_TaskInstances_Status ON TaskInstances(Status);
CREATE INDEX IX_TaskInstances_AssignedTo ON TaskInstances(AssignedTo);
CREATE INDEX IX_TaskInstances_StartedDate ON TaskInstances(StartedDate);

CREATE INDEX IX_ValidationResults_InstanceId ON ValidationResults(InstanceId);
CREATE INDEX IX_ValidationResults_IsValid ON ValidationResults(IsValid);

CREATE INDEX IX_ProcessMessages_ToUser ON ProcessMessages(ToUser);
CREATE INDEX IX_ProcessMessages_IsRead ON ProcessMessages(IsRead);

CREATE INDEX IX_WorkflowHistory_InstanceId ON WorkflowHistory(InstanceId);
CREATE INDEX IX_WorkflowHistory_ActionDate ON WorkflowHistory(ActionDate);

-- =============================================
-- Insert Validation Rules
-- =============================================


-- =============================================
-- Sample Views for Workflow Monitoring
-- =============================================
GO
-- View: Active Workflow Instances
CREATE VIEW vw_ActiveWorkflows AS
SELECT 
    pi.InstanceId,
    pi.ApplicationId,
    pd.ProcessName,
    pi.Status,
    td.TaskName AS CurrentTask,
    pi.StartedDate,
    pi.StartedBy,
    pi.Priority,
    DATEDIFF(HOUR, pi.StartedDate, GETUTCDATE()) AS HoursActive
FROM ProcessInstances pi
INNER JOIN ProcessDefinitions pd ON pi.ProcessId = pd.ProcessId
LEFT JOIN TaskDefinitions td ON pi.CurrentTaskId = td.TaskId
WHERE pi.Status = 'Active';
GO
-- View: Validation Status Summary
CREATE VIEW vw_ValidationStatus AS
SELECT 
    pi.InstanceId,
    pi.ApplicationId,
    COUNT(vr.ValidationId) AS TotalValidations,
    SUM(CASE WHEN vres.IsValid = 1 THEN 1 ELSE 0 END) AS PassedValidations,
    SUM(CASE WHEN vres.IsValid = 0 THEN 1 ELSE 0 END) AS FailedValidations,
    CASE 
        WHEN COUNT(vr.ValidationId) = SUM(CASE WHEN vres.IsValid = 1 THEN 1 ELSE 0 END) THEN 'All Passed'
        WHEN SUM(CASE WHEN vres.IsValid = 0 THEN 1 ELSE 0 END) > 0 THEN 'Has Failures'
        ELSE 'In Progress'
    END AS ValidationStatus
FROM ProcessInstances pi
CROSS JOIN ValidationRules vr
LEFT JOIN ValidationResults vres ON pi.InstanceId = vres.InstanceId AND vr.ValidationId = vres.ValidationId
WHERE vr.IsActive = 1
GROUP BY pi.InstanceId, pi.ApplicationId;
GO
-- View: Task Performance Metrics
CREATE VIEW vw_TaskPerformance AS
SELECT 
    td.TaskName,
    td.TaskType,
    td.TaskCategory,
    COUNT(ti.TaskInstanceId) AS TotalExecutions,
    AVG(CAST(ti.DurationMinutes AS FLOAT)) AS AvgDurationMinutes,
    td.EstimatedDurationMinutes,
    SUM(CASE WHEN ti.Status = 'Completed' THEN 1 ELSE 0 END) AS CompletedTasks,
    SUM(CASE WHEN ti.Status = 'Failed' THEN 1 ELSE 0 END) AS FailedTasks,
    CAST(SUM(CASE WHEN ti.Status = 'Completed' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(ti.TaskInstanceId) * 100 AS SuccessRate
FROM TaskDefinitions td
LEFT JOIN TaskInstances ti ON td.TaskId = ti.TaskId
GROUP BY td.TaskId, td.TaskName, td.TaskType, td.TaskCategory, td.EstimatedDurationMinutes;

GO

-- =============================================
-- Stored Procedures for Workflow Management
-- =============================================

-- Procedure: Start New Workflow Instance
CREATE PROCEDURE sp_StartWorkflowInstance
    @ProcessName NVARCHAR(100),
    @ApplicationId NVARCHAR(50),
    @StartedBy NVARCHAR(100),
    @Priority NVARCHAR(20) = 'Normal'
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE 1 INT;
    DECLARE @InstanceId INT = NEWID();
    DECLARE @StartTaskId INT;
    
    -- Get Process ID
    SELECT 1 = ProcessId 
    FROM ProcessDefinitions 
    WHERE ProcessName = @ProcessName AND IsActive = 1;
    
    IF 1 IS NULL
    BEGIN
        RAISERROR('Process definition not found: %s', 16, 1, @ProcessName);
        RETURN;
    END
    
    -- Get Start Task
    SELECT TOP 1 @StartTaskId = TaskId 
    FROM TaskDefinitions 
    WHERE ProcessId = 1 AND TaskType = 'Event' AND TaskCategory = 'Start'
    ORDER BY Sequence;
    
    -- Create Process Instance
    INSERT INTO ProcessInstances (InstanceId, ProcessId, ApplicationId, CurrentTaskId, StartedBy, Priority)
    VALUES (@InstanceId, 1, @ApplicationId, @StartTaskId, @StartedBy, @Priority);
    
    -- Log History
    INSERT INTO WorkflowHistory (InstanceId, Action, NewStatus, ActionBy, ActionReason)
    VALUES (@InstanceId, 'Workflow Started', 'Active', @StartedBy, 'New application submitted for processing');
    
    SELECT @InstanceId AS InstanceId;
END;
GO
-- Procedure: Complete Task
CREATE PROCEDURE sp_CompleteTask
    @InstanceId INT,
    @TaskName NVARCHAR(100),
    @CompletedBy NVARCHAR(100),
    @Result NVARCHAR(50) = 'Success',
    @ResultData NVARCHAR(MAX) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @TaskInstanceId INT;
    DECLARE @TaskId INT;
    DECLARE @NextTaskId INT;
    
    -- Get current task instance
    SELECT @TaskInstanceId = ti.TaskInstanceId, @TaskId = ti.TaskId
    FROM TaskInstances ti
    INNER JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
    WHERE ti.InstanceId = @InstanceId 
    AND td.TaskName = @TaskName 
    AND ti.Status IN ('Pending', 'InProgress');
    
    IF @TaskInstanceId IS NULL
    BEGIN
        RAISERROR('Task instance not found or already completed: %s', 16, 1, @TaskName);
        RETURN;
    END
    
    -- Complete the task
    UPDATE TaskInstances 
    SET Status = 'Completed',
        CompletedDate = GETUTCDATE(),
        Result = @Result,
        ResultData = @ResultData
    WHERE TaskInstanceId = @TaskInstanceId;
    
    -- Get next task based on flow
    SELECT TOP 1 @NextTaskId = tf.ToTaskId
    FROM TaskFlow tf
    WHERE tf.FromTaskId = @TaskId
    AND (tf.Condition IS NULL OR tf.Condition = @Result OR tf.IsDefault = 1)
    ORDER BY tf.IsDefault;
    
    -- Update process instance current task
    IF @NextTaskId IS NOT NULL
    BEGIN
        UPDATE ProcessInstances 
        SET CurrentTaskId = @NextTaskId
        WHERE InstanceId = @InstanceId;
        
        -- Create next task instance if not exists
        IF NOT EXISTS (SELECT 1 FROM TaskInstances WHERE InstanceId = @InstanceId AND TaskId = @NextTaskId)
        BEGIN
            INSERT INTO TaskInstances (InstanceId, TaskId, Status, StartedDate)
            VALUES (@InstanceId, @NextTaskId, 'Pending', GETUTCDATE());
        END
    END
    
    -- Log history
    INSERT INTO WorkflowHistory (InstanceId, TaskInstanceId, Action, NewStatus, ActionBy, Details)
    VALUES (@InstanceId, @TaskInstanceId, 'Task Completed: ' + @TaskName, 'Completed', @CompletedBy, @ResultData);
END;
GO
-- Procedure: Run Validation Check
CREATE PROCEDURE sp_RunValidationCheck
    @InstanceId INT,
    @ValidationCategory NVARCHAR(50) = NULL,
    @ValidatedBy NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ValidationId INT;
    DECLARE @ValidationName NVARCHAR(100);
    DECLARE @ValidationQuery NVARCHAR(MAX);
    DECLARE @ErrorMessage NVARCHAR(500);
    DECLARE @IsValid BIT;
    DECLARE @ValidationMessage NVARCHAR(500);
    DECLARE @SQL NVARCHAR(MAX);
    
    -- Cursor for validation rules
    DECLARE validation_cursor CURSOR FOR
    SELECT ValidationId, ValidationName, ValidationQuery, ErrorMessage
    FROM ValidationRules
    WHERE IsActive = 1 
    AND (@ValidationCategory IS NULL OR Category = @ValidationCategory);
    
    OPEN validation_cursor;
    FETCH NEXT FROM validation_cursor INTO @ValidationId, @ValidationName, @ValidationQuery, @ErrorMessage;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Execute validation query
        SET @SQL = 'SELECT @IsValid = (' + @ValidationQuery + ')';
        
        BEGIN TRY
            EXEC sp_executesql @SQL, N'@IsValid BIT OUTPUT', @IsValid OUTPUT;
            SET @ValidationMessage = CASE WHEN @IsValid = 1 THEN 'Validation passed' ELSE @ErrorMessage END;
        END TRY
        BEGIN CATCH
            SET @IsValid = 0;
            SET @ValidationMessage = 'Validation error: ' + ERROR_MESSAGE();
        END CATCH
        
        -- Insert or update validation result
        MERGE ValidationResults AS target
        USING (SELECT @InstanceId AS InstanceId, @ValidationId AS ValidationId) AS source
        ON target.InstanceId = source.InstanceId AND target.ValidationId = source.ValidationId
        WHEN MATCHED THEN
            UPDATE SET IsValid = @IsValid, 
            ValidationMessage = @ValidationMessage,
            ValidationDate = GETUTCDATE(),
            ValidatedBy = @ValidatedBy
        WHEN NOT MATCHED THEN
            INSERT (InstanceId, ValidationId, IsValid, ValidationMessage, ValidatedBy)
            VALUES (@InstanceId, @ValidationId, @IsValid, @ValidationMessage, @ValidatedBy);
        
        FETCH NEXT FROM validation_cursor INTO @ValidationId, @ValidationName, @ValidationQuery, @ErrorMessage;
    END
    
    CLOSE validation_cursor;
    DEALLOCATE validation_cursor;
    
    -- Return validation summary
    SELECT 
        vr.Category,
        COUNT(*) AS TotalChecks,
        SUM(CASE WHEN vres.IsValid = 1 THEN 1 ELSE 0 END) AS PassedChecks,
        SUM(CASE WHEN vres.IsValid = 0 THEN 1 ELSE 0 END) AS FailedChecks
    FROM ValidationRules vr
    INNER JOIN ValidationResults vres ON vr.ValidationId = vres.ValidationId
    WHERE vres.InstanceId = @InstanceId
    AND (@ValidationCategory IS NULL OR vr.Category = @ValidationCategory)
    GROUP BY vr.Category;
END;
GO
-- Procedure: Add Message
CREATE PROCEDURE sp_AddMessage
    @InstanceId INT,
    @FromUser NVARCHAR(100),
    @ToUser NVARCHAR(100) = NULL,
    @ToRole NVARCHAR(50) = NULL,
    @MessageType NVARCHAR(50) = 'Standard',
    @Subject NVARCHAR(200) = NULL,
    @MessageBody NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @MessageId INT = NEWID();
    
    INSERT INTO ProcessMessages (MessageId, InstanceId, FromUser, ToUser, ToRole, MessageType, Subject, MessageBody)
    VALUES (@MessageId, @InstanceId, @FromUser, @ToUser, @ToRole, @MessageType, @Subject, @MessageBody);
    
    -- Log history
    INSERT INTO WorkflowHistory (InstanceId, Action, ActionBy, Details)
    VALUES (@InstanceId, 'Message Sent', @FromUser, 'To: ' + ISNULL(@ToUser, @ToRole) + ' - ' + ISNULL(@Subject, 'No Subject'));
    
    SELECT @MessageId AS MessageId;
END;

GO
-- Procedure: Add Comment
CREATE PROCEDURE sp_AddComment
    @InstanceId INT,
    @TaskInstanceId INT = NULL,
    @CommentType NVARCHAR(50) = 'Internal',
    @CommentText NVARCHAR(MAX),
    @Author NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @CommentId INT = NEWID();
    
    INSERT INTO TaskComments (CommentId, InstanceId, TaskInstanceId, CommentType, CommentText, Author)
    VALUES (@CommentId, @InstanceId, @TaskInstanceId, @CommentType, @CommentText, @Author);
    
    -- Log history
    INSERT INTO WorkflowHistory (InstanceId, TaskInstanceId, Action, ActionBy, Details)
    VALUES (@InstanceId, @TaskInstanceId, 'Comment Added', @Author, LEFT(@CommentText, 200));
    
    SELECT @CommentId AS CommentId;
END;

GO
-- Procedure: Get Workflow Status
CREATE PROCEDURE sp_GetWorkflowStatus
    @InstanceId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Process Instance Info
    SELECT 
        pi.InstanceId,
        pi.ApplicationId,
        pi.KashrusCompanyId,
        pd.ProcessName,
        pi.Status,
        td.TaskName AS CurrentTask,
        td.TaskType AS CurrentTaskType,
        td.AssigneeRole AS CurrentAssignee,
        pi.StartedDate,
        pi.StartedBy,
        pi.Priority,
        DATEDIFF(HOUR, pi.StartedDate, GETUTCDATE()) AS HoursActive
    FROM ProcessInstances pi
    INNER JOIN ProcessDefinitions pd ON pi.ProcessId = pd.ProcessId
    LEFT JOIN TaskDefinitions td ON pi.CurrentTaskId = td.TaskId
    WHERE pi.InstanceId = @InstanceId;
    
    -- Validation Status
    SELECT 
        vr.Category,
        vr.ValidationName,
        vres.IsValid,
        vres.ValidationMessage,
        vres.ValidationDate,
        vres.ValidatedBy
    FROM ValidationRules vr
    LEFT JOIN ValidationResults vres ON vr.ValidationId = vres.ValidationId AND vres.InstanceId = @InstanceId
    WHERE vr.IsActive = 1
    ORDER BY vr.Category, vr.ValidationName;
    
    -- Task History
    SELECT 
        td.TaskName,
        ti.Status,
        ti.StartedDate,
        ti.CompletedDate,
        ti.DurationMinutes,
        ti.Result,
        ti.AssignedTo
    FROM TaskInstances ti
    INNER JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
    WHERE ti.InstanceId = @InstanceId
    ORDER BY ti.StartedDate;
    
    -- Recent ProcessMessages
    SELECT TOP 10
        m.FromUser,
        m.ToUser,
        m.ToRole,
        m.MessageType,
        m.Subject,
        m.MessageBody,
        m.SentDate,
        m.IsRead
    FROM ProcessMessages m
    WHERE m.InstanceId = @InstanceId
    ORDER BY m.SentDate DESC;
    
    -- Recent TaskComments
    SELECT TOP 10
        c.CommentType,
        c.CommentText,
        c.Author,
        c.CreatedDate,
        td.TaskName AS RelatedTask
    FROM TaskComments c
    LEFT JOIN TaskInstances ti ON c.TaskInstanceId = ti.TaskInstanceId
    LEFT JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
    WHERE c.InstanceId = @InstanceId AND c.IsVisible = 1
    ORDER BY c.CreatedDate DESC;
END;

GO
-- =============================================
-- Sample Data Insertion
-- =============================================

-- Create a sample workflow instance
DECLARE @SampleInstanceId INT;
EXEC sp_StartWorkflowInstance 
    @ProcessName = 'Admin Completion Workflow',
    @ApplicationId = 'APP-2025-0717-001',
    @StartedBy = 'J. Mitchell',
    @Priority = 'Normal';
GO
-- Insert some sample validation results
DECLARE @SampleProcessInstanceId INT;
SELECT TOP 1 @SampleProcessInstanceId = InstanceId 
FROM ProcessInstances 
WHERE ApplicationId = 'APP-2025-0717-001';
GO
-- Sample validation execution
EXEC sp_RunValidationCheck 
    @InstanceId = @SampleProcessInstanceId,
    @ValidatedBy = 'System';
GO
-- Sample message
EXEC sp_AddMessage
    @InstanceId = @SampleProcessInstanceId,
    @FromUser = 'J. Mitchell',
    @ToRole = 'Dispatcher',
    @Subject = 'Application Ready for Review',
    @MessageBody = 'Application ready for initial review. All documentation complete.';
GO
-- Sample comment
EXEC sp_AddComment
    @InstanceId = @SampleProcessInstanceId,
    @CommentType = 'Internal',
    @CommentText = 'Verified all ingredient certifications with suppliers. Coconut oil documentation updated.',
    @Author = 'J. Mitchell';

GO
-- =============================================
-- Function: Check All Validations Passed
-- =============================================

CREATE FUNCTION fn_AllValidationsPassed(@InstanceId INT)
RETURNS BIT
AS
BEGIN
    DECLARE @Result BIT = 0;
    
    IF NOT EXISTS (
        SELECT 1 
        FROM ValidationRules vr
        LEFT JOIN ValidationResults vres ON vr.ValidationId = vres.ValidationId AND vres.InstanceId = @InstanceId
        WHERE vr.IsActive = 1 
        AND (vres.IsValid IS NULL OR vres.IsValid = 0)
    )
    BEGIN
        SET @Result = 1;
    END
    
    RETURN @Result;
END;

GO
-- =============================================
-- Trigger: Auto-advance workflow on task completion
-- =============================================

CREATE TRIGGER tr_TaskCompletion_AutoAdvance
ON TaskInstances
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Only process when status changes to Completed
    IF UPDATE(Status)
    BEGIN
        DECLARE @InstanceId INT;
        DECLARE @TaskId INT;
        DECLARE @TaskName NVARCHAR(100);
        DECLARE @NextTaskId INT;
        
        -- Get completed tasks
        SELECT 
            i.InstanceId,
            i.TaskId,
            td.TaskName
        FROM inserted i
        INNER JOIN TaskDefinitions td ON i.TaskId = td.TaskId
        WHERE i.Status = 'Completed'
        AND NOT EXISTS (SELECT 1 FROM deleted d WHERE d.TaskInstanceId = i.TaskInstanceId AND d.Status = 'Completed');
        
        DECLARE task_cursor CURSOR FOR
        SELECT InstanceId, TaskId, TaskName FROM inserted 
        WHERE Status = 'Completed';
        
        OPEN task_cursor;
        FETCH NEXT FROM task_cursor INTO @InstanceId, @TaskId, @TaskName;
        
        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- For validation tasks, check if all validations in category passed
            IF @TaskName LIKE 'Validate_%'
            BEGIN
                DECLARE @Category NVARCHAR(50) = REPLACE(REPLACE(@TaskName, 'Validate_', ''), '_Data', '');
                
                -- Run validation check for this category
                EXEC sp_RunValidationCheck 
                    @InstanceId = @InstanceId,
                    @ValidationCategory = @Category,
                    @ValidatedBy = 'System';
            END
            
            -- Check for auto-advance to next task
            SELECT TOP 1 @NextTaskId = tf.ToTaskId
            FROM TaskFlow tf
            INNER JOIN TaskDefinitions td ON tf.ToTaskId = td.TaskId
            WHERE tf.FromTaskId = @TaskId
            AND td.AutoComplete = 1;
            
            IF @NextTaskId IS NOT NULL
            BEGIN
                -- Auto-complete next task if it's a system task
                INSERT INTO TaskInstances (InstanceId, TaskId, Status, StartedDate, CompletedDate, Result)
                VALUES (@InstanceId, @NextTaskId, 'Completed', GETUTCDATE(), GETUTCDATE(), 'Success');
            END
            
            FETCH NEXT FROM task_cursor INTO @InstanceId, @TaskId, @TaskName;
        END
        
        CLOSE task_cursor;
        DEALLOCATE task_cursor;
    END
END;

GO
-- =============================================
-- Performance and Monitoring Views
-- =============================================

-- View: Workflow Dashboard
CREATE VIEW vw_WorkflowDashboard AS
SELECT 
    'Total Active Workflows' AS Metric,
    COUNT(*) AS Value,
    'Count' AS Unit
FROM ProcessInstances 
WHERE Status = 'Active'

UNION ALL

SELECT 
    'Average Hours to Complete',
    AVG(CAST(DATEDIFF(HOUR, StartedDate, CompletedDate) AS FLOAT)),
    'Hours'
FROM ProcessInstances 
WHERE Status = 'Completed' AND CompletedDate IS NOT NULL

UNION ALL

SELECT 
    'Pending Admin Tasks',
    COUNT(*),
    'Count'
FROM TaskInstances ti
INNER JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
WHERE ti.Status = 'Pending' AND td.AssigneeRole = 'Admin'

UNION ALL

SELECT 
    'Failed Validations',
    COUNT(*),
    'Count'
FROM ValidationResults 
WHERE IsValid = 0 AND ValidationDate >= DATEADD(DAY, -7, GETUTCDATE());

GO
-- View: Bottleneck Analysis
CREATE VIEW vw_BottleneckAnalysis AS
SELECT 
    td.TaskName,
    td.AssigneeRole,
    COUNT(ti.TaskInstanceId) AS PendingTasks,
    AVG(CAST(DATEDIFF(HOUR, ti.StartedDate, GETUTCDATE()) AS FLOAT)) AS AvgHoursPending,
    td.EstimatedDurationMinutes / 60.0 AS EstimatedHours
FROM TaskInstances ti
INNER JOIN TaskDefinitions td ON ti.TaskId = td.TaskId
WHERE ti.Status = 'Pending'
GROUP BY td.TaskName, td.AssigneeRole, td.EstimatedDurationMinutes
HAVING COUNT(ti.TaskInstanceId) > 0
ORDER BY PendingTasks DESC, AvgHoursPending DESC;

GO
-- =============================================
-- Cleanup and Maintenance Procedures
-- =============================================

-- Procedure: Archive Completed Workflows
CREATE PROCEDURE sp_ArchiveCompletedWorkflows
    @DaysOld INT = 90
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @CutoffDate DATETIME2 = DATEADD(DAY, -@DaysOld, GETUTCDATE());
    DECLARE @ArchivedCount INT = 0;
    
    -- Archive completed workflows older than specified days
    UPDATE ProcessInstances 
    SET Status = 'Archived'
    WHERE Status = 'Completed' 
    AND CompletedDate < @CutoffDate;
    
    SET @ArchivedCount = @@ROWCOUNT;
    
    SELECT @ArchivedCount AS ArchivedWorkflows;
END;
GO
PRINT 'Admin Completion Workflow DDL and stored procedures created successfully!';
PRINT 'Database schema includes:';
PRINT '- Process and Task Definitions';
PRINT '- Workflow Instance Management';
PRINT '- Validation Framework';
PRINT '- Communication System';
PRINT '- Audit and History Tracking';
PRINT '- Performance Monitoring Views';
PRINT '- Sample data and test procedures';
PRINT '';
PRINT 'Key stored procedures:';
PRINT '- sp_StartWorkflowInstance';
PRINT '- sp_CompleteTask';
PRINT '- sp_RunValidationCheck';
PRINT '- sp_GetWorkflowStatus';
PRINT '- sp_AddMessage';
PRINT '- sp_AddComment';