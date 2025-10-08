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
IF OBJECT_ID('sp_add_flow', 'P') IS NOT NULL DROP PROCEDURE sp_add_flow;
IF OBJECT_ID('sp_StartWorkflowInstance', 'P') IS NOT NULL DROP PROCEDURE sp_StartWorkflowInstance;
IF OBJECT_ID('sp_CompleteTask', 'P') IS NOT NULL DROP PROCEDURE sp_CompleteTask;
IF OBJECT_ID('sp_RunValidationCheck', 'P') IS NOT NULL DROP PROCEDURE sp_RunValidationCheck;
IF OBJECT_ID('sp_AddMessage', 'P') IS NOT NULL DROP PROCEDURE IF EXISTS sp_AddMessage;
IF OBJECT_ID('sp_AddComment', 'P') IS NOT NULL DROP PROCEDURE sp_AddComment;
IF OBJECT_ID('sp_GetWorkflowStatus', 'P') IS NOT NULL DROP PROCEDURE sp_GetWorkflowStatus;
GO
-- Truncate child tables first (tables with foreign keys)
IF OBJECT_ID('WorkflowHistory', 'U') IS NOT NULL DELETE FROM WorkflowHistory;
IF OBJECT_ID('TaskComments', 'U') IS NOT NULL DELETE FROM TaskComments;
IF OBJECT_ID('ProcessMessages', 'U') IS NOT NULL DELETE FROM ProcessMessages;
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
IF OBJECT_ID('TaskAlerts', 'U') IS NOT NULL DELETE FROM TaskAlerts;
GO
-- Drop child tables first (tables with foreign keys)
if OBJECT_ID('TaskAlerts', 'U') IS NOT NULL DROP TABLE TaskAlerts;
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
GO
-- Drop parent tables (tables with primary keys referenced by others)
IF OBJECT_ID('LaneRoles', 'U') IS NOT NULL DROP TABLE LaneRoles;
IF OBJECT_ID('StageStatus', 'U') IS NOT NULL DROP TABLE StageStatus;
IF OBJECT_ID('TaskCommentTypes', 'U') IS NOT NULL DROP TABLE TaskCommentTypes;
IF OBJECT_ID('ProcessMessageTypes', 'U') IS NOT NULL DROP TABLE ProcessMessageTypes;
IF OBJECT_ID('ValidationRules', 'U') IS NOT NULL DROP TABLE ValidationRules;
IF OBJECT_ID('ProcessDefinitions', 'U') IS NOT NULL DROP TABLE ProcessDefinitions;
IF OBJECT_ID('ProcessStatus', 'U') IS NOT NULL DROP TABLE ProcessStatus;
IF OBJECT_ID('ProcessPriorities', 'U') IS NOT NULL DROP TABLE IF EXISTS ProcessPriorities;
GO
PRINT 'All tables, views, procedures, functions, and triggers dropped successfully.';

-- ==================================
-- Workflow Process Definitions
-- ==================================
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
    Description NVARCHAR(500), -- user instructions or details
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy NVARCHAR(100) NOT NULL,
    ModifiedDate DATETIME2,
    ModifiedBy NVARCHAR(100),
    PreScriptJson NVARCHAR(MAX), -- PRE JSON configuration for task-specific settings
    PostScriptJson NVARCHAR(MAX), -- POST JSON configuration for task-specific settings
    FOREIGN KEY (TaskCategory) REFERENCES TaskCategories(TaskCategoryCode),
    FOREIGN KEY (TaskType) REFERENCES TaskTypes(TaskTypeCode),
    FOREIGN KEY (LaneId) REFERENCES LaneDefinitions(LaneId),
    FOREIGN KEY (ProcessId) REFERENCES ProcessDefinitions(ProcessId)
);
-- Add additional columns to TaskDefinitions for Pre and Post processing
-- ALTER TABLE TaskDefinitions 
-- ADD 
    --CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    --CreatedBy NVARCHAR(100) NOT NULL,
    --ModifiedDate DATETIME2,
    --ModifiedBy NVARCHAR(100),
    --PreScriptJson NVARCHAR(MAX), -- PRE JSON configuration for task-specific settings
    --PostScriptJson NVARCHAR(MAX); -- POST JSON configuration for task-specific settings

-- Task Dependencies and Flow
CREATE TABLE TaskFlow (
    FlowId INT IDENTITY(1,1) PRIMARY KEY,
    FromTaskId INT,
    ToTaskId INT NOT NULL,
    Condition NVARCHAR(500), -- Conditional logic for flow
    IsDefault BIT NOT NULL DEFAULT 0, -- default path if no conditions met
    FOREIGN KEY (FromTaskId) REFERENCES TaskDefinitions(TaskId),
    FOREIGN KEY (ToTaskId) REFERENCES TaskDefinitions(TaskId)
);
GO
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

-- ==================================
-- Application Workflow Instances
-- Only 1 Process per ApplicationId
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
    FOREIGN KEY (Status) REFERENCES ProcessStatus(StatusCode)
    --FOREIGN KEY (ProcessId) REFERENCES ProcessDefinitions(ProcessId)
    --FOREIGN KEY (CurrentTaskId) REFERENCES TaskDefinitions(TaskId)
);

-- Stage Status Lookup Table
CREATE TABLE StageStatus (
    StatusCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    StatusDescription NVARCHAR(255) NOT NULL
);

-- Stage Instance is a specific instance of a Lane within a process
-- We get the Role from the LaneDefinitions
-- Each StageInstance is linked to a ProcessInstance
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



-- Task Instance Execution
-- Task instance is linked to TaskDefinition and StageInstance
CREATE TABLE TaskInstances (
    TaskInstanceId INT IDENTITY(1,1) PRIMARY KEY,
    TaskId INT NOT NULL, -- TaskDefinition
    StageId INT NOT NULL, -- StageInstance
    Status NVARCHAR(20) NOT NULL DEFAULT 'Pending', -- 'Pending', 'InProgress', 'Completed', 'Failed', 'Skipped'
    AssignedTo NVARCHAR(100),
    StartedDate DATETIME2,
    CompletedDate DATETIME2,
    #DurationMinutes AS DATEDIFF(MINUTE, StartedDate, CompletedDate),
    Result NVARCHAR(50), -- 'Success', 'Failed', 'Retry', 'Skip'
    ResultData NVARCHAR(MAX), -- JSON result user state data
    ErrorMessage NVARCHAR(1000),
    RetryCount INT DEFAULT 0,
    FOREIGN KEY (Status) REFERENCES TaskStatus(StatusCode),
    FOREIGN KEY (StageId) REFERENCES StageInstance(StageInstanceId),
    FOREIGN KEY (TaskId) REFERENCES TaskDefinitions(TaskId)
);

-- this is used to track tasks with a timer process 
-- the script engine will insert PENDING and resolve when Completed
-- We can add a rule for overdue tasks to send or add WFMessage or set flags
-- set_task_alert(task_instance_id, 'Reminder', 'Task is overdue', due_date | duration_minutes)
CREATE TABLE TaskAlert (
    AlertId INT IDENTITY(1,1) PRIMARY KEY,
    TaskInstanceId INT NOT NULL,
    AlertType NVARCHAR(20) NOT NULL DEFAULT 'Escalation', -- 'Reminder', 'Escalation', 'Timeout'
    AlertMessage NVARCHAR(500) NOT NULL,
    StartDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    DueDate DATETIME2 NOT NULL,
    IsResolved BIT NOT NULL DEFAULT 0,
    ResolvedDate DATETIME2,
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
    FOREIGN KEY (ProcessInstanceId) REFERENCES ProcessInstances(InstanceId),
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

CREATE INDEX IX_ProcessMessages_ToUser ON ProcessMessages(ToUser);
CREATE INDEX IX_ProcessMessages_IsRead ON ProcessMessages(IsRead);

CREATE INDEX IX_WorkflowHistory_InstanceId ON WorkflowHistory(InstanceId);
CREATE INDEX IX_WorkflowHistory_ActionDate ON WorkflowHistory(ActionDate);
GO
-- =============================================