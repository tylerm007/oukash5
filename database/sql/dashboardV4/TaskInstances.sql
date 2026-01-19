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
IF OBJECT_ID('dbo.StageInstance', 'U') IS NOT NULL DROP TABLE dbo.StageInstance; -- REMOVED IN THIS REVISION
IF OBJECT_ID('dbo.StageStatus', 'U') IS NOT NULL DROP TABLE dbo.StageStatus;
IF OBJECT_ID('dbo.ProcessInstances', 'U') IS NOT NULL DROP TABLE dbo.ProcessInstances;
IF OBJECT_ID('dbo.ProcessStatus', 'U') IS NOT NULL DROP TABLE dbo.ProcessStatus;
IF OBJECT_ID('dbo.ProcessPriorities', 'U') IS NOT NULL DROP TABLE dbo.ProcessPriorities;
GO

-- StageStatus is needed to determine valid statuses for StageInstance
CREATE TABLE [dbo].[StageStatus](
	[StatusCode] [nvarchar](20) NOT NULL,
	[StatusDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

-- StageInstance is tied to each Application workflow stage
--CREATE TABLE [dbo].[StageInstance](
--	[StageInstanceId] [int] IDENTITY(1,1) NOT NULL,
--	[ApplicationId] [int] NOT NULL,
--	[StageDefinitionId] [int] NOT NULL,
--	[Status] [nvarchar](20) NOT NULL,
--	[StartedDate] [datetime2](7) NULL,
--	[CompletedDate] [datetime2](7) NULL,
--	
--PRIMARY KEY CLUSTERED 
--(
--	[StageInstanceId] ASC
--)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
--) ON [PRIMARY]
--GO

--ALTER TABLE [dbo].[StageInstance] ADD  DEFAULT 'NEW' FOR [Status]
--GO

--ALTER TABLE [dbo].[StageInstance]  WITH CHECK ADD FOREIGN KEY([StageDefinitionId])
--REFERENCES [dbo].[StageDefinitions] ([StageId])
--GO

--ALTER TABLE [dbo].[StageInstance]  WITH CHECK ADD FOREIGN KEY([Status])
--REFERENCES [dbo].[StageStatus] ([StatusCode])
--GO


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
	[TaskDefinitionId] [int] NOT NULL,
	[ApplicationId] [int] NOT NULL,
	[StageId] [int] NOT NULL,
	[Status] [nvarchar](20) NOT NULL,
	[AssignedTo] [nvarchar](100) NULL,
	[CompletedBy] [nvarchar](100) NULL,
	[CompletedCapacity] [nvarchar](100) NULL,
	[StartedDate] [datetime2](7) NULL,
	[CompletedDate] [datetime2](7) NULL,
	[DurationMinutes]  AS (datediff(minute,[StartedDate],[CompletedDate])),
	[Result] [nvarchar](50) NULL,
	[ResultData] [nvarchar](max) NULL,
	[ErrorMessage] [nvarchar](1000) NULL,
	[RetryCount] [int] NULL,
	[ModifiedDate][datetime2](7) NULL,
PRIMARY KEY CLUSTERED
(
	[TaskInstanceId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[TaskInstances] ADD  DEFAULT 'PENDING' FOR [Status]
GO

ALTER TABLE [dbo].[TaskInstances] ADD  DEFAULT 0 FOR [RetryCount]
GO

ALTER TABLE [dbo].[TaskInstances]  WITH CHECK ADD FOREIGN KEY([StageId])
REFERENCES [dbo].[StageDefinitions] ([StageId])
GO

ALTER TABLE [dbo].[TaskInstances]  WITH CHECK ADD FOREIGN KEY([Status])
REFERENCES [dbo].[TaskStatus] ([StatusCode])
GO

ALTER TABLE [dbo].[TaskInstances]  WITH CHECK ADD FOREIGN KEY([TaskDefinitionId])
REFERENCES [dbo].[TaskDefinitions] ([TaskId])
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



-- Drop AssignedTo column if it exists
IF EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[TaskInstances]') AND name = 'AssignedTo')
BEGIN
    ALTER TABLE [dbo].[TaskInstances] DROP COLUMN [AssignedTo];
END
GO

-- Add columns if they don't exist (for existing tables)
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[TaskInstances]') AND name = 'TaskRole')
BEGIN
    ALTER TABLE [dbo].[TaskInstances] ADD [TaskRole] nvarchar(100) NULL;
END
GO

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[TaskInstances]') AND name = 'CompletedBy')
BEGIN
    ALTER TABLE [dbo].[TaskInstances] ADD [CompletedBy] nvarchar(100) NULL;
END
GO

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[TaskInstances]') AND name = 'CompletedCapacity')
BEGIN
    ALTER TABLE [dbo].[TaskInstances] ADD [CompletedCapacity] nvarchar(100) NULL;
END
GO