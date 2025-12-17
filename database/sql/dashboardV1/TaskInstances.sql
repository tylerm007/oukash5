USE [dashboard]
GO

/****** Object:  Table [dbo].[ProcessInstances]    Script Date: 11/25/2025 3:05:49 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- Drop existing tables if they exist (in reverse dependency order)
IF OBJECT_ID('dbo.WorkflowHistory', 'U') IS NOT NULL DROP TABLE dbo.WorkflowHistory;
IF OBJECT_ID('dbo.TaskInstances', 'U') IS NOT NULL DROP TABLE dbo.TaskInstances;
IF OBJECT_ID('dbo.TaskStatus', 'U') IS NOT NULL DROP TABLE dbo.TaskStatus;
IF OBJECT_ID('dbo.StageInstance', 'U') IS NOT NULL DROP TABLE dbo.StageInstance;
IF OBJECT_ID('dbo.StageStatus', 'U') IS NOT NULL DROP TABLE dbo.StageStatus;
IF OBJECT_ID('dbo.ProcessInstances', 'U') IS NOT NULL DROP TABLE dbo.ProcessInstances;
IF OBJECT_ID('dbo.ProcessStatus', 'U') IS NOT NULL DROP TABLE dbo.ProcessStatus;
IF OBJECT_ID('dbo.ProcessPriorities', 'U') IS NOT NULL DROP TABLE dbo.ProcessPriorities;
GO

CREATE TABLE [dbo].[ProcessPriorities](
	[PriorityCode] [nvarchar](10) NOT NULL,
	[PriorityDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[PriorityCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[ProcessStatus](
	[StatusCode] [nvarchar](10) NOT NULL,
	[StatusDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[ProcessInstances](
	[InstanceId] [int] IDENTITY(1,1) NOT NULL,
	[ProcessId] [int] NOT NULL,
	[ApplicationId] [int] NOT NULL,
	[Status] [nvarchar](10) NOT NULL,
	[CurrentTaskId] [int] NULL,
	[StartedDate] [datetime2](7) NOT NULL,
	[StartedBy] [nvarchar](100) NOT NULL,
	[CompletedDate] [datetime2](7) NULL,
	[CompletedBy] [nvarchar](100) NULL,
	[Priority] [nvarchar](10) NULL,
	[ContextData] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[InstanceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[ProcessInstances] ADD  DEFAULT ('NEW') FOR [Status]
GO

ALTER TABLE [dbo].[ProcessInstances] ADD  DEFAULT (getutcdate()) FOR [StartedDate]
GO

ALTER TABLE [dbo].[ProcessInstances] ADD  DEFAULT ('NORMAL') FOR [Priority]
GO

ALTER TABLE [dbo].[ProcessInstances]  WITH CHECK ADD FOREIGN KEY([Priority])
REFERENCES [dbo].[ProcessPriorities] ([PriorityCode])
GO

ALTER TABLE [dbo].[ProcessInstances]  WITH CHECK ADD FOREIGN KEY([Status])
REFERENCES [dbo].[ProcessStatus] ([StatusCode])
GO


CREATE TABLE [dbo].[StageStatus](
	[StatusCode] [nvarchar](20) NOT NULL,
	[StatusDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Eliminate this when we flatten - use StageDefinitions instead to feed StageInstances
CREATE TABLE [dbo].[StageInstance](
	[StageInstanceId] [int] IDENTITY(1,1) NOT NULL,
	[ProcessInstanceId] [int] NOT NULL,
	[LaneId] [int] NOT NULL,
	[Status] [nvarchar](20) NOT NULL,
	[StartedDate] [datetime2](7) NULL,
	[CompletedDate] [datetime2](7) NULL,
	[DurationDays]  AS (datediff(day,[StartedDate],[CompletedDate])),
	[RetryCount] [int] NULL,
	[AssignedTo] [nvarchar](100) NULL,
	[AssignedBy] [nvarchar](100) NULL,
	[AssignedDate] [datetime2](7) NULL,
	[CompletedCount] [int] NULL,
	[TotalCount] [int] NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[StageInstanceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[StageInstance] ADD  DEFAULT ('NEW') FOR [Status]
GO

ALTER TABLE [dbo].[StageInstance] ADD  DEFAULT (getutcdate()) FOR [CreatedDate]
GO

ALTER TABLE [dbo].[StageInstance] ADD  DEFAULT ('System') FOR [CreatedBy]
GO

ALTER TABLE [dbo].[StageInstance]  WITH CHECK ADD FOREIGN KEY([LaneId])
REFERENCES [dbo].[LaneDefinitions] ([LaneId])
GO

ALTER TABLE [dbo].[StageInstance]  WITH CHECK ADD FOREIGN KEY([ProcessInstanceId])
REFERENCES [dbo].[ProcessInstances] ([InstanceId])
GO

ALTER TABLE [dbo].[StageInstance]  WITH CHECK ADD FOREIGN KEY([Status])
REFERENCES [dbo].[StageStatus] ([StatusCode])
GO


CREATE TABLE [dbo].[TaskStatus](
	[StatusCode] [nvarchar](20) NOT NULL,
	[StatusDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[TaskInstances](
	[TaskInstanceId] [int] IDENTITY(1,1) NOT NULL,
	[TaskId] [int] NOT NULL,
	[StageId] [int] NOT NULL,
	[Status] [nvarchar](20) NOT NULL,
	[AssignedTo] [nvarchar](100) NULL,
	[StartedDate] [datetime2](7) NULL,
	[CompletedDate] [datetime2](7) NULL,
	[#DurationMinutes]  AS (datediff(minute,[StartedDate],[CompletedDate])),
	[Result] [nvarchar](50) NULL,
	[ResultData] [nvarchar](max) NULL,
	[ErrorMessage] [nvarchar](1000) NULL,
	[RetryCount] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[TaskInstanceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[TaskInstances] ADD  DEFAULT ('Pending') FOR [Status]
GO

ALTER TABLE [dbo].[TaskInstances] ADD  DEFAULT ((0)) FOR [RetryCount]
GO

ALTER TABLE [dbo].[TaskInstances]  WITH CHECK ADD FOREIGN KEY([StageId])
REFERENCES [dbo].[StageInstance] ([StageInstanceId])
GO

ALTER TABLE [dbo].[TaskInstances]  WITH CHECK ADD FOREIGN KEY([Status])
REFERENCES [dbo].[TaskStatus] ([StatusCode])
GO

ALTER TABLE [dbo].[TaskInstances]  WITH CHECK ADD FOREIGN KEY([TaskId])
REFERENCES [dbo].[TaskDefinitions] ([TaskId])
GO



-- Process Status
INSERT INTO ProcessStatus (StatusCode, StatusDescription) VALUES
('NEW', 'New Process Instance'),
('RUNNING', 'Process Currently Running'),
('COMPLETED', 'Process Completed Successfully'),
('FAILED', 'Process Failed'),
('SUSPENDED', 'Process Suspended'),
('TERMINATED', 'Process Terminated');
GO

-- Process Priorities
INSERT INTO ProcessPriorities (PriorityCode, PriorityDescription) VALUES
('LOW', 'Low Priority'),
('NORMAL', 'Normal Priority'),
('HIGH', 'High Priority'),
('URGENT', 'Urgent Priority');
GO

-- Stage Status
INSERT INTO StageStatus (StatusCode, StatusDescription) VALUES
('NEW', 'New Stage'),
('IN_PROGRESS', 'Stage In Progress'),
('COMPLETED', 'Stage Completed'),
('ON_HOLD', 'Stage On Hold'),
('CANCELLED', 'Stage Cancelled');
GO

-- Task Status
INSERT INTO TaskStatus (StatusCode, StatusDescription) VALUES
('PENDING', 'Task Pending Execution'),
('RUNNING', 'Task Currently Running'),
('COMPLETED', 'Task Completed Successfully'),
('FAILED', 'Task Failed'),
('SKIPPED', 'Task Skipped'),
('NEW', 'New Task Created'),
('ON_HOLD', 'Task On Hold'),    
('CANCELLED', 'Task Cancelled');
GO

-- Woekflow History Table may not be needed if we use the temporal feature - it is an AUdit table of state change
CREATE TABLE [dbo].[WorkflowHistory](
	[HistoryId] [int] IDENTITY(1,1) NOT NULL,
	[InstanceId] [int] NOT NULL,
	[TaskInstanceId] [int] NULL,
	[Action] [nvarchar](100) NOT NULL,
	[PreviousStatus] [nvarchar](50) NULL,
	[NewStatus] [nvarchar](50) NULL,
	[ActionBy] [nvarchar](100) NOT NULL,
	[ActionDate] [datetime2](7) NOT NULL,
	[ActionReason] [nvarchar](500) NULL,
	[Details] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[HistoryId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[WorkflowHistory] ADD  DEFAULT (getutcdate()) FOR [ActionDate]
GO

ALTER TABLE [dbo].[WorkflowHistory]  WITH CHECK ADD FOREIGN KEY([InstanceId])
REFERENCES [dbo].[ProcessInstances] ([InstanceId])
GO

ALTER TABLE [dbo].[WorkflowHistory]  WITH CHECK ADD FOREIGN KEY([TaskInstanceId])
REFERENCES [dbo].[TaskInstances] ([TaskInstanceId])
GO
