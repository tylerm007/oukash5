USE [dashboardV1]
GO

-- Drop tables in correct order (child tables first, parent tables last)
IF OBJECT_ID('dbo.TaskFlow', 'U') IS NOT NULL DROP TABLE dbo.TaskFlow;
IF OBJECT_ID('dbo.TaskDefinitions', 'U') IS NOT NULL DROP TABLE dbo.TaskDefinitions;
IF OBJECT_ID('dbo.LaneDefinitions', 'U') IS NOT NULL DROP TABLE dbo.LaneDefinitions;
IF OBJECT_ID('dbo.StageDefinitions', 'U') IS NOT NULL DROP TABLE dbo.StageDefinitions;
IF OBJECT_ID('dbo.ProcessDefinitions', 'U') IS NOT NULL DROP TABLE dbo.ProcessDefinitions;
IF OBJECT_ID('dbo.TaskTypes', 'U') IS NOT NULL DROP TABLE dbo.TaskTypes;    
IF OBJECT_ID('dbo.TaskCategories', 'U') IS NOT NULL DROP TABLE dbo.TaskCategories;
IF OBJECT_ID('dbo.LaneRoles', 'U') IS NOT NULL DROP TABLE dbo.LaneRoles;
GO
--
-- Create BPMN Related Tables to define a workflow process - once a BPMN model is finalized, these tables will be populated
-- it becomes a static cache that is loaded into memory for execution of the BPMN process engine
 --

/****** Script Date: 11/25/2025 2:33:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- TaskCategories Table: Defines the categories of tasks in BPMN processes  
CREATE TABLE [dbo].[TaskCategories](
	[TaskCategoryCode] [nvarchar](20) NOT NULL,
	[TaskCategoryDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[TaskCategoryCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

-- TaskTypes Table: Defines the types of tasks in BPMN processes
CREATE TABLE [dbo].[TaskTypes](
	[TaskTypeCode] [nvarchar](20) NOT NULL,
	[TaskTypeDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[TaskTypeCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


-- LaneRoles Table: Defines the roles associated with lanes in BPMN processes
CREATE TABLE [dbo].[LaneRoles](
	[RoleCode] [nvarchar](20) NOT NULL,
	[RoleDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[RoleCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Table: ProcessDefinitions The root definitions of BPMN processes
CREATE TABLE [dbo].[ProcessDefinitions](
	[ProcessId] [int] IDENTITY(1,1) NOT NULL,
	[ProcessName] [nvarchar](100) NOT NULL,
	[ProcessVersion] [nvarchar](10) NOT NULL,
	[Description] [nvarchar](500) NULL,
	[IsActive] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL  DEFAULT (getutcdate()),
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[ProcessId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[ProcessDefinitions] ADD  DEFAULT ('1.0') FOR [ProcessVersion]
GO

ALTER TABLE [dbo].[ProcessDefinitions] ADD  DEFAULT ((1)) FOR [IsActive]
GO

ALTER TABLE [dbo].[ProcessDefinitions] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO


----- Table: LaneDefinitions Definitions of lanes within a BPMN process
CREATE TABLE [dbo].[LaneDefinitions](
	[LaneId] [int] IDENTITY(1,1) NOT NULL,
	[ProcessId] [int] NOT NULL,
	[LaneName] [nvarchar](100) NOT NULL,
	[LaneDescription] [nvarchar](500) NULL,
	[EstimatedDurationDays] [int] NULL,
	[LaneRole] [nvarchar](20) NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL DEFAULT (getutcdate()),	
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[LaneId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[LaneDefinitions] ADD  DEFAULT ('NCRC') FOR [LaneRole]
GO

ALTER TABLE [dbo].[LaneDefinitions] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO

ALTER TABLE [dbo].[LaneDefinitions]  WITH CHECK ADD FOREIGN KEY([LaneRole])
REFERENCES [dbo].[LaneRoles] ([RoleCode])
GO

ALTER TABLE [dbo].[LaneDefinitions]  WITH CHECK ADD FOREIGN KEY([ProcessId])
REFERENCES [dbo].[ProcessDefinitions] ([ProcessId])
GO


CREATE TABLE [dbo].[StageDefinitions](
	[StageId] [int] IDENTITY(1,1) NOT NULL,
	[StageName] [nvarchar](100) NOT NULL,
	[StageDescription] [nvarchar](500) NULL,
	[EstimatedDurationDays] [int] NULL,
	[CreatedDate] [datetime2](7) NOT NULL DEFAULT (getutcdate()),
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[StageId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[StageDefinitions] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO




-- TaskDefinitions Table: Definitions of tasks (action) to be completed within a BPMN process
CREATE TABLE [dbo].[TaskDefinitions](
	[TaskId] [int] IDENTITY(1,1) NOT NULL,
	[ProcessId] [int] NOT NULL,
	[TaskName] [nvarchar](100) NOT NULL,
	[TaskType] [nvarchar](20) NOT NULL,
	[TaskCategory] [nvarchar](20) NULL,
	[Sequence] [int] NOT NULL,
	[LaneId] [int] NOT NULL,
	[IsParallel] [bit] NOT NULL,
	[AssigneeRole] [nvarchar](20) NULL,
	[EstimatedDurationMinutes] [int] NULL,
	[IsRequired] [bit] NOT NULL,
	[AutoComplete] [bit] NOT NULL,
	[Description] [nvarchar](500) NULL,
 	[CreatedDate] [datetime2](7) NOT NULL DEFAULT (getutcdate()),
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
	[PreScriptJson] [nvarchar](max) NULL,
	[PostScriptJson] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[TaskId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[TaskDefinitions] ADD  DEFAULT ((0)) FOR [IsParallel]
GO

ALTER TABLE [dbo].[TaskDefinitions] ADD  DEFAULT ((1)) FOR [IsRequired]
GO

ALTER TABLE [dbo].[TaskDefinitions] ADD  DEFAULT ((0)) FOR [AutoComplete]
GO

ALTER TABLE [dbo].[TaskDefinitions] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO

ALTER TABLE [dbo].[TaskDefinitions]  WITH CHECK ADD FOREIGN KEY([LaneId])
REFERENCES [dbo].[LaneDefinitions] ([LaneId])
GO

ALTER TABLE [dbo].[TaskDefinitions]  WITH CHECK ADD FOREIGN KEY([ProcessId])
REFERENCES [dbo].[ProcessDefinitions] ([ProcessId])
GO

ALTER TABLE [dbo].[TaskDefinitions]  WITH CHECK ADD FOREIGN KEY([TaskCategory])
REFERENCES [dbo].[TaskCategories] ([TaskCategoryCode])
GO

ALTER TABLE [dbo].[TaskDefinitions]  WITH CHECK ADD FOREIGN KEY([TaskType])
REFERENCES [dbo].[TaskTypes] ([TaskTypeCode])
GO



CREATE TABLE [dbo].[TaskFlow](
	[FlowId] [int] IDENTITY(1,1) NOT NULL,
	[FromTaskId] [int] NULL,
	[ToTaskId] [int] NOT NULL,
	[Condition] [nvarchar](500) NULL,
	[IsDefault] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[FlowId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[TaskFlow] ADD  DEFAULT ((0)) FOR [IsDefault]
GO

ALTER TABLE [dbo].[TaskFlow]  WITH CHECK ADD FOREIGN KEY([FromTaskId])
REFERENCES [dbo].[TaskDefinitions] ([TaskId])
GO

ALTER TABLE [dbo].[TaskFlow]  WITH CHECK ADD FOREIGN KEY([ToTaskId])
REFERENCES [dbo].[TaskDefinitions] ([TaskId])
GO


-- Lane Roles (if not already exist)
INSERT INTO LaneRoles (RoleCode, RoleDescription) VALUES
('NCRC', 'NCRC Coordinator'),
('NCRCADMIN', 'NCRC Administrator'),
('DISPATCH', 'Dispatcher Role'),
('ADMIN', 'System Administrator'),
('LEGAL', 'Legal Department'),
('INSP', 'Inspection Team'),
('IAR', 'Ingredients Review Team'),
('PROD', 'Products Department'),
('RC', 'Rabbinical Coordinator'),
('CERT', 'Certification Team'),
('BILLING', 'Billing Department'),
('IAR_MANAGER', 'IAR Manager'),
('PROD_MANAGER', 'Products Manager'),
('RC_MANAGER', 'RC Manager'),
('RFR', 'Rabbinical Field Representative'),
('SYSTEM', 'System Automated');
GO


-- Task Types
INSERT INTO TaskTypes (TaskTypeCode, TaskTypeDescription) VALUES
('CONFIRM', 'User Confirmation Task - Requires human interaction'),
('ACTION', 'User Action Task - Requires human interaction'),
('USER', 'User Task - Requires human interaction'),
('SYSTEM', 'System Task - Automated execution'),
('START', 'Process Start Event'),
('END', 'Process End Event'),
('SERVICE', 'Service Task - External service call'),
('SCRIPT', 'Script Task - Executes a script'),
('CONDITION', 'Condition Task - Evaluates a condition'),
('LANESTART','Subprocess Lane Start'),
('LANEEND','Subprocess Lane End'),
('PROGRESS', 'Subprocess Progress'),
('GATEWAY', 'Gateway - Decision point');
GO

-- Task Categories
INSERT INTO TaskCategories (TaskCategoryCode, TaskCategoryDescription) VALUES
('REVIEW', 'Review and Analysis Tasks'),
('ASSIGNMENT', 'Task Assignment Activities'),
('COMMUNICATION', 'Communication and Correspondence'),
('APPROVAL', 'Approval and Authorization'),
('COMPLETION', 'Task Completion Activities'),
('FINANCIAL', 'Financial and Billing Tasks'),
('ESCALATION', 'Escalation and Exception Handling'),
('NOTIFICATION', 'System Notifications'),
('CONFIRMATION', 'User Confirmation'),
('SCHEDULING', 'Scheduling and Planning'),
('INPUT', 'Data Input and Entry'),
('SELECTOR', 'Selection and Decision Making'),
('SUBPROCESS','Internal processing only'),
('PROGRESS_TASK', 'Subprocess Progress'),
('VERIFICATION', 'Data and Status Verification');
GO


-- =============================================
-- 1. ProcessDefinition Insert
-- =============================================
INSERT INTO ProcessDefinitions (ProcessName, ProcessVersion, Description, IsActive, CreatedBy)
VALUES ('OU Application Init', '1.0', 'OU Kosher initial application process', 1, 'SYSTEM');
GO
-- =============================================
-- 2. LaneDefinition Inserts
-- =============================================
INSERT INTO LaneDefinitions (ProcessId, LaneName, LaneDescription, EstimatedDurationDays, LaneRole, CreatedBy)
VALUES 
(1, 'Initial', 'Initial application review and task assignment', 2, 'NCRC', 'system'),
(1, 'NDA', 'Non-disclosure agreement handling and execution', 3, 'LEGAL', 'system'),
(1, 'Inspection', 'Plant inspection and RFR assignment process', 10, 'RC', 'system'),
(1, 'Ingredients', 'IAR ingredients and kosher code review process', 7, 'IAR', 'system'),
(1, 'Products', 'Product evaluation and PLA processing', 5, 'PROD', 'system'),
(1, 'Contract', 'Contract review and certification agreement', 3, 'LEGAL', 'system'),
(1, 'Certification', 'Final certification and invoice processing', 2, 'CERT', 'system');
GO

INSERT INTO StageDefinitions (StageName, StageDescription, EstimatedDurationDays, CreatedBy)
VALUES 
('Initial', 'Initial application review and task assignment', 2,'system'),
('NDA', 'Non-disclosure agreement handling and execution', 3,  'system'),
('Inspection', 'Plant inspection and RFR assignment process', 10,  'system'),
('Ingredients', 'IAR ingredients and kosher code review process', 7,  'system'),
('Products', 'Product evaluation and PLA processing', 5,'system'),
('Contract', 'Contract review and certification agreement', 3,  'system'),
('Certification', 'Final certification and invoice processing', 2,  'system');
GO
-- Load task_definitions.sql for each stage and task flow