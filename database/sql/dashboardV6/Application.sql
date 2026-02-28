USE [dashboard]
GO

/****** Object:  Table [dbo].[WF_Applications]    Script Date: 11/25/2025 3:59:22 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- Drop tables in correct order (children first, then parents)
IF OBJECT_ID('dbo.EventAction', 'U') IS NOT NULL DROP TABLE [dbo].[EventAction];
IF OBJECT_ID('dbo.RoleAssigment', 'U') IS NOT NULL DROP TABLE [dbo].[RoleAssigment];
IF OBJECT_ID('dbo.WF_ApplicationMessages', 'U') IS NOT NULL DROP TABLE [dbo].[WF_ApplicationMessages];
IF OBJECT_ID('dbo.WF_QuoteItems', 'U') IS NOT NULL DROP TABLE [dbo].[WF_QuoteItems];
IF OBJECT_ID('dbo.WF_Quotes', 'U') IS NOT NULL DROP TABLE [dbo].[WF_Quotes];
IF OBJECT_ID('dbo.WF_QuoteStatus', 'U') IS NOT NULL DROP TABLE [dbo].[WF_QuoteStatus];
IF OBJECT_ID('dbo.WF_Files', 'U') IS NOT NULL DROP TABLE [dbo].[WF_Files];
IF OBJECT_ID('dbo.WF_FileTypes', 'U') IS NOT NULL DROP TABLE [dbo].[WF_FileTypes];
IF OBJECT_ID('dbo.WF_Applications', 'U') IS NOT NULL DROP TABLE [dbo].[WF_Applications];
IF OBJECT_ID('dbo.WF_Priorities', 'U') IS NOT NULL DROP TABLE [dbo].[WF_Priorities];
IF OBJECT_ID('dbo.WF_ApplicationStatus', 'U') IS NOT NULL DROP TABLE [dbo].[WF_ApplicationStatus];
GO

CREATE TABLE [dbo].[WF_ApplicationStatus](
	[StatusCode] [nvarchar](50) NOT NULL,
	[StatusDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[WF_Priorities](
	[PriorityCode] [nvarchar](20) NOT NULL,
	[PriorityDescription] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[PriorityCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[WF_Applications](
	[ApplicationID] [int] IDENTITY(1,1) NOT NULL,
	[ApplicationNumber] [int] NULL, -- Link to existing JotForm Application Number
	[CompanyID] [int] NOT NULL DEFAULT 0, -- CompanyTB
	[PlantID] [int] NULL, -- PlantTB
	[ExternalAppRef][int] NULL, -- Parent Ref SubmissionApplcation
	[WFLinkedApp] [int] NULL, -- Link to either submission or workflow application
	[ApplicationType] [nvarchar](10) NULL, -- Default WORKFLOW or SUBMISSION
	[SubmissionDate] [date] NOT NULL, -- date from JotForm
	[Status] [nvarchar](50) NOT NULL,
	[Priority] [nvarchar](20) NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[ApplicationID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],

UNIQUE NONCLUSTERED 
(
	[ApplicationNumber] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]

GO

--ALTER TABLE [dbo].[WF_Applications] ADD  [ExternalAppRef] [int] NULL
--ALTER TABLE [dbo].[WF_Applications] ADD  [WFLnkedApp] [int] NULL
--GO
--ALTER TABLE [dbo].[WF_Applications] ADD  [ApplicationType] [nvarchar](10) NULL
--GO

ALTER TABLE [dbo].[WF_Applications] ADD  DEFAULT getdate() FOR [SubmissionDate]
GO

ALTER TABLE [dbo].[WF_Applications] ADD  DEFAULT 'NEW' FOR [Status]
GO

ALTER TABLE [dbo].[WF_Applications] ADD  DEFAULT 'NORMAL' FOR [Priority]
GO

ALTER TABLE [dbo].[WF_Applications] ADD  DEFAULT getutcdate() FOR [CreatedDate]
GO

ALTER TABLE [dbo].[WF_Applications] ADD  DEFAULT 'System' FOR [CreatedBy]
GO


ALTER TABLE [dbo].[WF_Applications]  WITH CHECK ADD FOREIGN KEY([Priority])
REFERENCES [dbo].[WF_Priorities] ([PriorityCode])
GO

ALTER TABLE [dbo].[WF_Applications]  WITH CHECK ADD FOREIGN KEY([Status])
REFERENCES [dbo].[WF_ApplicationStatus] ([StatusCode])
GO

ALTER TABLE [dbo].[TaskInstances]  WITH CHECK ADD FOREIGN KEY([ApplicationId])
REFERENCES [dbo].[WF_Applications] ([ApplicationID])
GO


CREATE TABLE [dbo].[WF_FileTypes](
	[FileType] [nvarchar](5) NOT NULL,
	[FileTypeName] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[FileType] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO



CREATE TABLE [dbo].[WF_Files](
	[FileID] [int] IDENTITY(1,1) NOT NULL,
	[ApplicationID] [int] NOT NULL,
	[FileName] [nvarchar](500) NOT NULL,
	[FileType] [nvarchar](5) NOT NULL,
	[FileSize] [nvarchar](20) NULL,
	[UploadedDate] [date] NOT NULL,
	[Tag] [nvarchar](200) NULL,
	[IsProcessed] [bit] NOT NULL,
	[RecordCount] [int] NULL,
	[FilePath] [nvarchar](1000) NULL,
	[CCreatedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[FileID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_Files] ADD  DEFAULT 0 FOR [IsProcessed]
GO

ALTER TABLE [dbo].[WF_Files] ADD  DEFAULT getutcdate() FOR [CCreatedDate]
GO

ALTER TABLE [dbo].[WF_Files] ADD  DEFAULT 'System' FOR [CreatedBy]
GO

ALTER TABLE [dbo].[WF_Files]  WITH CHECK ADD FOREIGN KEY([ApplicationID])
REFERENCES [dbo].[WF_Applications] ([ApplicationID])
GO

ALTER TABLE [dbo].[WF_Files]  WITH CHECK ADD FOREIGN KEY([FileType])
REFERENCES [dbo].[WF_FileTypes] ([FileType])
GO




CREATE TABLE [dbo].[WF_QuoteStatus](
	[StatusCode] [nvarchar](10) NOT NULL,
	[StatusDesc] [nvarchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[StatusCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[WF_Quotes](
	[QuoteID] [int] IDENTITY(1,1) NOT NULL,
	[ApplicationID] [int] NOT NULL,
	[QuoteNumber] [nvarchar](50) NOT NULL,
	[TotalAmount] [decimal](10, 2) NOT NULL,
	[ValidUntil] [date] NOT NULL,
	[Status] [nvarchar](10) NOT NULL,
	[LastUpdatedDate] [date] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](100) NOT NULL,
	[ModifiedDate] [datetime2](7) NULL,
	[ModifiedBy] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[QuoteID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[QuoteNumber] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_Quotes] ADD  DEFAULT 'PEND' FOR [Status]
GO

ALTER TABLE [dbo].[WF_Quotes] ADD  DEFAULT getutcdate() FOR [CreatedDate]
GO

ALTER TABLE [dbo].[WF_Quotes] ADD  DEFAULT 'System' FOR [CreatedBy]
GO

ALTER TABLE [dbo].[WF_Quotes]  WITH CHECK ADD FOREIGN KEY([ApplicationID])
REFERENCES [dbo].[WF_Applications] ([ApplicationID])
GO

ALTER TABLE [dbo].[WF_Quotes]  WITH CHECK ADD FOREIGN KEY([Status])
REFERENCES [dbo].[WF_QuoteStatus] ([StatusCode])
GO



CREATE TABLE [dbo].[WF_QuoteItems](
	[QuoteItemID] [int] IDENTITY(1,1) NOT NULL,
	[QuoteID] [int] NOT NULL,
	[Description] [nvarchar](500) NOT NULL,
	[Amount] [decimal](10, 2) NOT NULL,
	[SortOrder] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[QuoteItemID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_QuoteItems] ADD  DEFAULT 1 FOR [SortOrder]
GO

ALTER TABLE [dbo].[WF_QuoteItems]  WITH CHECK ADD FOREIGN KEY([QuoteID])
REFERENCES [dbo].[WF_Quotes] ([QuoteID])
GO




CREATE TABLE [dbo].[WF_ApplicationMessages](
	[MessageID] [int] IDENTITY(1,1) NOT NULL,
	[ApplicationID] [int] NOT NULL,
	[FromUser] [nvarchar](100) NOT NULL,
	[ToUser] [nvarchar](100) NULL,
	[MessageText] [nvarchar](max) NOT NULL,
	[MessageType] [nvarchar](50) NOT NULL,
	[Priority] [nvarchar](20) NOT NULL,
	[SentDate] [datetime2](7) NOT NULL,
	[TaskInstanceId] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[MessageID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_ApplicationMessages] ADD  DEFAULT 'internal' FOR [MessageType]
GO

ALTER TABLE [dbo].[WF_ApplicationMessages] ADD  DEFAULT 'NORMAL' FOR [Priority]
GO

ALTER TABLE [dbo].[WF_ApplicationMessages] ADD  DEFAULT getdate() FOR [SentDate]
GO

ALTER TABLE [dbo].[WF_ApplicationMessages]  WITH CHECK ADD FOREIGN KEY([ApplicationID])
REFERENCES [dbo].[WF_Applications] ([ApplicationID])
GO

--ALTER TABLE [dbo].[WF_ApplicationMessages]  WITH CHECK ADD FOREIGN KEY([FromUser])
--REFERENCES [dbo].[WF_Users] ([Username])
--GO

ALTER TABLE [dbo].[WF_ApplicationMessages]  WITH CHECK ADD FOREIGN KEY([Priority])
REFERENCES [dbo].[WF_Priorities] ([PriorityCode])
GO


CREATE TABLE [dbo].[RoleAssigment](
	[RoleAssigmentID] [int] IDENTITY(1,1) NOT NULL,
	[ApplicationId] [int] NOT NULL,
	[Role] [nvarchar](10) NOT NULL,
	[Assignee] [nvarchar](100) NOT NULL,
	[IsPrimary]	 [bit] DEFAULT 1 NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[CreatedBy] [nvarchar](32) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[RoleAssigmentID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[RoleAssigment] ADD  DEFAULT getutcdate() FOR [CreatedDate]
GO

ALTER TABLE [dbo].[RoleAssigment] ADD  DEFAULT 'System' FOR [CreatedBy]
GO

ALTER TABLE [dbo].[RoleAssigment]  WITH CHECK ADD FOREIGN KEY([ApplicationId])
REFERENCES [dbo].[WF_Applications] ([ApplicationID])
GO
-- Added IsPrimary column to indicate if this is the primary assignee for the role
-- ALTER TABLE RoleAssignmet add  IsPrimary bit default 1 not null
--GO
--ALTER TABLE [dbo].[RoleAssigment]  WITH CHECK ADD FOREIGN KEY([Assignee])
--REFERENCES [dbo].[WF_Users] ([Username])
--GO

--ALTER TABLE [dbo].[RoleAssigment]  WITH CHECK ADD FOREIGN KEY([Role])
--REFERENCES [dbo].[WF_Roles] ([UserRole])
--GO



-- Used by background process to keep track of Paid Invoices

CREATE TABLE [dbo].[EventAction](
	[EventId] [int] IDENTITY(1,1) NOT NULL,
	[EventKey] [nvarchar](250) NOT NULL,
	[TaskInstanceId] [int] NOT NULL,
	[EventStatus] [nvarchar](20) NOT NULL,
	[EventType] [nvarchar](20) NOT NULL,
	[EventMessage] [nvarchar](500) NOT NULL,
	[StartDate] [datetime2](7) NOT NULL,
	[DueDate] [datetime2](7) NULL,
	[IsResolved] [bit] NOT NULL,
	[ResolvedDate] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[EventId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[EventAction] ADD  DEFAULT 'PENDING' FOR [EventStatus]
GO

ALTER TABLE [dbo].[EventAction] ADD  DEFAULT 'External' FOR [EventType]
GO

ALTER TABLE [dbo].[EventAction] ADD  DEFAULT getutcdate() FOR [StartDate]
GO

ALTER TABLE [dbo].[EventAction] ADD  DEFAULT 0 FOR [IsResolved]
GO

ALTER TABLE [dbo].[EventAction]  WITH CHECK ADD FOREIGN KEY([TaskInstanceId])
REFERENCES [dbo].[TaskInstances] ([TaskInstanceId])
GO



INSERT INTO WF_ApplicationStatus (StatusCode, StatusDescription) VALUES
    ('NEW', 'Application is new'),
    ('INC', 'Application is incomplete'),
    ('DISP', 'Application has been dispatched for review'),
    ('INP', 'Application is currently being processed - assign NCRC'),
    ('PAYPEND', 'Payment Pending'),
    ('CONTRACT', 'Contract SENT'),
    ('INSPECTION', 'Inspection Scheduled'),
    ('REVIEW', 'Inspection Report Submitted to IAR'),
    ('COMPL', 'Application processing is certified'),
    ('WTH', 'Application has been Withdrawn');
GO

INSERT INTO WF_Priorities (PriorityCode, PriorityDescription) VALUES
    ('LOW', 'Low Priority'),
    ('NORMAL', 'Normal Priority'),
    ('HIGH', 'High Priority'),
    ('CRITICAL', 'Critical Priority');
GO

INSERT INTO WF_QuoteStatus (StatusCode, StatusDesc) VALUES
('PEND','Pending Acceptance'),
('REJECT', 'Rejected'),
('ACC','Accepted');
GO

INSERT INTO WF_FileTypes (FileType, FileTypeName) VALUES
('APP', 'Application'),
('ING', 'Ingredients'),
('PROD', 'Products'),
('PDF', 'PDF Document'),
('IMG', 'Image File'),
('JPG', 'JPG Image'),
('PNG', 'PNG Image'),
('DOC', 'Word Document'),
('XLS', 'Excel Spreadsheet'),
('OTHER', 'Other');
GO

-- New table used by GUI

CREATE TABLE [dbo].[WF_UserProfile](
	[Username] [nvarchar](100) NOT NULL,
	[Profile] [text] NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[LastModDate] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
