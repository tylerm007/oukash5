USE [dashboardv1]
GO

/****** Object:  Table [dbo].[WF_Users]    Script Date: 11/25/2025 5:03:54 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- Drop tables in correct order (child tables first, then parent tables)
IF OBJECT_ID('dbo.WF_USER_ROLE', 'U') IS NOT NULL
	DROP TABLE [dbo].[WF_USER_ROLE];
GO

IF OBJECT_ID('dbo.WF_USER_ADMINS', 'U') IS NOT NULL
	DROP TABLE [dbo].[WF_USER_ADMINS];
GO

IF OBJECT_ID('dbo.WF_Roles', 'U') IS NOT NULL
	DROP TABLE [dbo].[WF_Roles];
GO

IF OBJECT_ID('dbo.WF_Users', 'U') IS NOT NULL
	DROP TABLE [dbo].[WF_Users];
GO

CREATE TABLE [dbo].[WF_Users](
	[Username] [nvarchar](100) NOT NULL,
	[Email] [nvarchar](255) NOT NULL,
	[FullName] [nvarchar](200) NOT NULL,
	[IsActive] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
	[LastLoginDate] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_Users] ADD  DEFAULT 1 FOR [IsActive]
GO

ALTER TABLE [dbo].[WF_Users] ADD  DEFAULT getdate() FOR [CreatedDate]
GO



CREATE TABLE [dbo].[WF_Roles](
	[UserRole] [nvarchar](10) NOT NULL,
	[Role] [nvarchar](50) NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[UserRole] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_Roles] ADD  DEFAULT getdate() FOR [CreatedDate]
GO



CREATE TABLE [dbo].[WF_USER_ROLE](
	[UserName] [nvarchar](100) NOT NULL,
	[UserRole] [nvarchar](10) NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[UserName] ASC,
	[UserRole] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_USER_ROLE] ADD  DEFAULT getdate() FOR [CreatedDate]
GO

ALTER TABLE [dbo].[WF_USER_ROLE]  WITH CHECK ADD FOREIGN KEY([UserName])
REFERENCES [dbo].[WF_Users] ([Username])
GO

ALTER TABLE [dbo].[WF_USER_ROLE]  WITH CHECK ADD FOREIGN KEY([UserRole])
REFERENCES [dbo].[WF_Roles] ([UserRole])
GO


CREATE TABLE [dbo].[WF_USER_ADMINS](
	[UserName] [nvarchar](100) NOT NULL,
	[AdminUserName] [nvarchar](100) NOT NULL,
	[IsPrimary] [bit] NOT NULL,
	[CreatedDate] [datetime2](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[UserName] ASC,
	[AdminUserName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[WF_USER_ADMINS] ADD  DEFAULT 0 FOR [IsPrimary]
GO

ALTER TABLE [dbo].[WF_USER_ADMINS] ADD  DEFAULT getdate() FOR [CreatedDate]
GO

ALTER TABLE [dbo].[WF_USER_ADMINS]  WITH CHECK ADD FOREIGN KEY([AdminUserName])
REFERENCES [dbo].[WF_Users] ([Username])
GO

ALTER TABLE [dbo].[WF_USER_ADMINS]  WITH CHECK ADD FOREIGN KEY([UserName])
REFERENCES [dbo].[WF_Users] ([Username])
GO

INSERT INTO WF_Roles (UserRole, Role) VALUES
    ('ADMIN', 'Administrator'),
    ('DISPATCH', 'Dispatcher'),
    ('LEGAL','Legal'),
    ('IAR', 'Ingredients'),
    ('PROD','Product'),
    ('RFR', 'RFR'),
    ('SALES', 'Sales'),
    ('SUPPORT', 'Support'),
    ('CUST', 'Customer'),
    ('NCRC-ADMIN', 'NCRC Admin'),
    ('RC','RC'),
    ('FIN', 'Finance'),
    ('GUEST', 'Guest'),
    ('NCRC', 'NCRC');

GO

insert into WF_Users (Username, Email, FullName) values
('Rabbi Dick', 'dick@ou.org', 'Rabbi Dick'),
('Rabbi Epstein', 'epstein@ou.org', 'Rabbi Epstein'),
('Rabbi Gutterman', 'gutterman@ou.org', 'Rabbi Gutterman'),
('Rabbi Nosenchuk', 'nosenchuk@ou.org', 'Rabbi Nosenchuk'),
('Rabbi Rabinowitz', 'rabinowitz@ou.org', 'Rabbi Rabinowitz'),
('Rabbi Shkarofsky', 'shkarofsky@ou.org', 'Rabbi Shkarofsky'),
('Rabbi Stareshefsky', 'stareshefsky@ou.org', 'Rabbi Stareshefsky'),
('Rabbi Steinberg', 'steinberg@ou.org', 'Rabbi Steinberg'),
('Rabbi Machuca', 'machuca@ou.org', 'Rabbi Machuca'),
('Rabbi Twersky', 'twersky@ou.org', 'Rabbi Twersky'),
-- Insert Admin users
('Bassie Fogelman', 'bfogelman@ou.org', 'Bassie Fogelman'),
('Tikki Goldstein', 'tgoldstein@ou.org', 'Tikki Goldstein'),
('Aviva Gottesman', 'agottesman@ou.org', 'Aviva Gottesman'),
('Miriam Ganz', 'mganz@ou.org', 'Miriam Ganz'),
('Naomi Marcovici', 'nmarcovici@ou.org', 'Naomi Marcovici'),
('Yael Schottenstein', 'yschottenstein@ou.org', 'Yael Schottenstein'),
('J.Sanders', 'jsanders@ou.org', 'J. Sanders'),
('TYLER.BAND', 'tyler.band@ou.org', 'Tyler Band'),
('SHOUKI.BENJAMIN', 'shouki.benjamin@ou.org', 'Shouki Benjamin'),
('gmagder', 'gmagder@ou.org', 'Gary Magder');

GO

INSERT INTO WF_USER_ADMINS (UserName, AdminUserName, IsPrimary) VALUES
('Rabbi Dick', 'Bassie Fogelman', 1),
--('Rabbi Epstein', 'TBD', 0),
('Rabbi Gutterman', 'Bassie Fogelman', 1),
('Rabbi Nosenchuk', 'Tikki Goldstein', 1),
('Rabbi Rabinowitz', 'Aviva Gottesman', 1),
('Rabbi Shkarofsky', 'Miriam Ganz', 1),
('Rabbi Stareshefsky', 'Naomi Marcovici', 1),
('Rabbi Steinberg', 'Yael Schottenstein', 1),
--('Rabbi Machuca', 'TBD', 0),
('Rabbi Twersky', 'Yael Schottenstein', 1);
GO

-- SWITCH TO USER_TABLE/PESON_JOB, PERSON_TB
INSERT INTO WF_USER_ROLE (UserName, UserRole) VALUES
('Rabbi Dick', 'NCRC'),
('Rabbi Epstein', 'NCRC'),
('Rabbi Gutterman', 'NCRC'),
('Rabbi Nosenchuk', 'NCRC'),
('Rabbi Rabinowitz', 'NCRC'),
('Rabbi Shkarofsky', 'NCRC'),
('Rabbi Stareshefsky', 'NCRC'),
('Rabbi Steinberg', 'NCRC'),
('Rabbi Machuca', 'NCRC'),
('Rabbi Twersky', 'NCRC'),
-- Insert Admin users
('Bassie Fogelman', 'NCRC-ADMIN'),
('Tikki Goldstein', 'NCRC-ADMIN'),
('Aviva Gottesman', 'NCRC-ADMIN'),
('Miriam Ganz', 'NCRC-ADMIN'),
('Naomi Marcovici', 'NCRC-ADMIN'),
('Yael Schottenstein', 'NCRC-ADMIN'),
('SHOUKI.BENJAMIN', 'NCRC-ADMIN'),
('SHOUKI.BENJAMIN', 'NCRC'),
('SHOUKI.BENJAMIN', 'DISPATCH'),
('TYLER.BAND','DISPATCH'),
('TYLER.BAND','NCRC'),
('TYLER.BAND','IAR'),
('TYLER.BAND', 'LEGAL'),
('TYLER.BAND', 'PROD'),
('TYLER.BAND', 'RFR');
GO