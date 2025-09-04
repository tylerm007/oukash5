-- =============================================
-- NCRC Application Management Database Schema
-- MS SQL Server DDL with Sample Data
-- =============================================

-- Create Database

-- CREATE DATABASE NCRC_ApplicationManagement;
-- USE NCRC_ApplicationManagement;
use dashboard;
-- =============================================
-- DROP TABLES (for clean setup)
-- =============================================
-- Drop child tables first (tables with foreign keys)
DROP TABLE IF EXISTS WF_ActivityLog;
DROP TABLE IF EXISTS WF_ApplicationComments;
DROP TABLE IF EXISTS WF_ApplicationMessages;
DROP TABLE IF EXISTS WF_Files;
DROP TABLE IF EXISTS WF_QuoteItems;
DROP TABLE IF EXISTS WF_Quotes;
DROP TABLE IF EXISTS WF_Ingredients;
DROP TABLE IF EXISTS WF_Products;
DROP TABLE IF EXISTS WF_Plants;
DROP TABLE IF EXISTS WF_Contacts;
DROP TABLE IF EXISTS WF_Companies;
DROP TABLE IF EXISTS WF_Applications;
DROP TABLE IF EXISTS WF_Users;

-- Drop parent/reference tables
DROP TABLE IF EXISTS WF_Dashboard;
DROP TABLE IF EXISTS WF_FileTypes;
DROP TABLE IF EXISTS WF_ActivityStatus;
DROP TABLE IF EXISTS WF_QuoteStatus;
DROP TABLE IF EXISTS WF_ApplicationStatus;
DROP TABLE IF EXISTS WF_Priorities;
DROP TABLE IF EXISTS WF_Roles;

-- =============================================
-- CREATE TABLES
-- =============================================

CREATE TABLE WF_Roles (
    UserRole NVARCHAR(10) PRIMARY KEY,
    Role NVARCHAR(50) NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE()
);

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
    ('NCRC', 'NCRC');

-- Users Table
CREATE TABLE WF_Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(100) NOT NULL UNIQUE,
    FullName NVARCHAR(200) NOT NULL,
    Email NVARCHAR(255) NOT NULL UNIQUE,
    Role NVARCHAR(10) NOT NULL DEFAULT 'ADMIN', -- technically a User can have many roles
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    LastLoginDate DATETIME2 NULL, -- add to OKTA /auth/login on success callback
    FOREIGN KEY (Role) REFERENCES WF_Roles(UserRole)
);

-- This could be the parent table to do counts and sums or we write a View 
CREATE TABLE WF_Dashboard (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    count_new INT DEFAULT 0, -- applications status Rule.count(WF_Applications where status='NEW')
    count_in_progress INT DEFAULT 0,
    count_withdrawn INT  DEFAULT 0,
    count_completed INT  DEFAULT 0,
    count_overdue INT  DEFAULT 0,
    total_count INT  DEFAULT 0
);
-- Root Record 
INSERT INTO WF_Dashboard ( count_new, count_in_progress, count_withdrawn, count_completed, count_overdue, total_count)   
VALUES ( 1, 0, 0, 0, 0, 1);

CREATE TABLE WF_ApplicationStatus (
    StatusCode NVARCHAR(50) NOT NULL PRIMARY KEY,
    StatusDescription NVARCHAR(255) NOT NULL
);
INSERT INTO WF_ApplicationStatus (StatusCode, StatusDescription) VALUES
    ('NEW', 'Application is new'),
    ('INC', 'Application is incomplete'),
    ('DISP', 'Application has been dispatched for review'),
    ('INP', 'Application is currently being processed'),
    ('COMPL', 'Application processing is completed'),
    ('REV', 'Application requires further review'),
    ('WTH', 'Application has been withdrawn');

CREATE TABLE WF_Priorities (
    PriorityCode NVARCHAR(20) NOT NULL PRIMARY KEY,
    PriorityDescription NVARCHAR(255) NOT NULL
);  

INSERT INTO WF_Priorities (PriorityCode, PriorityDescription) VALUES
    ('LOW', 'Low Priority'),
    ('NORMAL', 'Normal Priority'),
    ('HIGH', 'High Priority'),
    ('CRITICAL', 'Critical Priority');

-- WF_Applications Table
CREATE TABLE WF_Applications (
    ApplicationID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationNumber INT NOT NULL UNIQUE, -- ties back to legacy CompanyApplication.ID 
    CompanyID INT NOT NULL,
    PlantID INT, -- becomes OWNSID CompanyID-PlantID
    SubmissionDate DATE NOT NULL,
    Status NVARCHAR(50) NOT NULL DEFAULT 'NEW',
    Priority NVARCHAR(20) DEFAULT 'NORMAL', -- 'Low', 'Normal', 'High', 'Critical'
    AssignedTo nvarchar(100) NULL, -- User email
    AssignedBy nvarchar(100) NULL, -- User email
    AssignedDate datetime2(7) NULL, -- Rule.formula when AssignedTo is not null return current_date
    CreatedDate datetime2(7) NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy nvarchar(100) NOT NULL DEFAULT 'System',
    ModifiedDate datetime2(7) NULL,
    ModifiedBy nvarchar(100) NULL,
    WFDashboardID INT NULL DEFAULT 1,
    FOREIGN KEY (WFDashboardID) REFERENCES WF_Dashboard(ID),
    FOREIGN KEY (Priority) REFERENCES WF_Priorities(PriorityCode),
    FOREIGN KEY (Status) REFERENCES WF_ApplicationStatus(StatusCode)
    --,FOREIGN KEY (CompanyID) REFERENCES COMPANYTB(CompanyID)
    --,FOREIGN KEY (PlantID) REFERENCES PLANTTB(PlantID)
);


-- When Application is NEW - Rule,after_flush_event we can copy data to this table using key ()
-- Companies Table - JOIN OU_KASH.COMPANY_TB
CREATE TABLE WF_Companies (
    CompanyID INT IDENTITY(1,1) PRIMARY KEY, 
    ApplicationID INT NOT NULL,
    KashrusCompanyID INT NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
    --,FOREIGN KEY (KashrusCompanyID) REFERENCES COMPANYTB(CompanyID)
);


-- Contacts Table -- not sure where to get this
CREATE TABLE WF_Contacts (
    ContactID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

-- Plants Table 
CREATE TABLE WF_Plants (
    PlantID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    PlantNumber INT  NULL, -- Foreign Key to ou_kash.PLANT_TB
    CreatedDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
    --,FOREIGN KEY (PlantNumber) REFERENCES PLANTTB(PlantID)
);


-- Create table: WF_Products
CREATE TABLE [dbo].[WF_Products] (
    [ProductID] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [ApplicationID] INT NOT NULL,
    [action] NVARCHAR(100) NOT NULL DEFAULT 'Add',
    [legacyId] NVARCHAR(50) NOT NULL, -- LINK to PRODUCTSTB ???
    [doNotImport] BIT NOT NULL DEFAULT 0,
    [message] NVARCHAR(MAX) NULL,
    [labelType] NVARCHAR(100) NOT NULL, -- lookups ???
    [labelName] NVARCHAR(100) NOT NULL,
    [brandName] NVARCHAR(100) NOT NULL,
    [labelCompanyId] NVARCHAR(50) NOT NULL, -- lookup??
    [distributorName] NVARCHAR(150) NOT NULL,
    [group] NVARCHAR(10) NOT NULL,
    [symbol] NVARCHAR(20) NOT NULL,
    [dpm] NVARCHAR(50) NOT NULL,
    [category] NVARCHAR(100) NOT NULL, -- LOOKUP ???
    [usePlantStatus] BIT NOT NULL,
    [status] NVARCHAR(50) NOT NULL, -- LOOKUP ???
    [legacyStatus] NVARCHAR(MAX) NULL,
    [consumer] BIT NOT NULL,
    [industrial] BIT NOT NULL,
    [finalized] BIT NOT NULL,
    [processedBy] NVARCHAR(100) NOT NULL,
    [processedDate] DATE NOT NULL,
    [notes] NVARCHAR(255) NOT NULL,
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

-- Add indexes for common queries
CREATE INDEX [IX_WF_Products_Status] ON [dbo].[WF_Products] ([status]);
CREATE INDEX [IX_WF_Products_DPM] ON [dbo].[WF_Products] ([dpm]);
CREATE INDEX [IX_WF_Products_Group] ON [dbo].[WF_Products] ([group]);
CREATE INDEX [IX_WF_Products_ProcessedDate] ON [dbo].[WF_Products] ([processedDate]);




CREATE TABLE WF_Ingredients (
    IngredientID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL, 
    Source NVARCHAR(100) NOT NULL,
    UKDId NVARCHAR(50) NULL,
    RMC NVARCHAR(50) NULL,
    IngredientName NVARCHAR(200) NOT NULL,
    Manufacturer NVARCHAR(200) NOT NULL,
    Brand NVARCHAR(200) NOT NULL,
    Packaging NVARCHAR(50) NOT NULL,
    Agency NVARCHAR(20) NOT NULL,
    AddedDate DATE NOT NULL,
    AddedBy NVARCHAR(100) NOT NULL,
    Status NVARCHAR(50) NOT NULL,
    NCRCId NVARCHAR(50) NOT NULL,
    CreatedDate DATETIME2 DEFAULT GETDATE(),
    ModifiedDate DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

-- Create indexes for better performance
CREATE INDEX IX_WF_Ingredients_NCRCId ON WF_Ingredients(NCRCId);
CREATE INDEX IX_WF_Ingredients_Status ON WF_Ingredients(Status);
CREATE INDEX IX_WF_Ingredients_AddedDate ON WF_Ingredients(AddedDate);
CREATE INDEX IX_WF_Ingredients_Agency ON WF_Ingredients(Agency);

CREATE TABLE WF_QuoteStatus(
	StatusCode NVARCHAR(10) NOT NULL PRIMARY KEY,
	StatusDesc NVARCHAR(50)
);

INSERT INTO WF_QuoteStatus (StatusCode, StatusDesc) VALUES
('PEND','Pending Acceptance'),
('REJECT', 'Rejected'),
('ACC','Accepted');

-- Quotes Table
CREATE TABLE WF_Quotes (
    QuoteID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    QuoteNumber NVARCHAR(50) NOT NULL UNIQUE,
    TotalAmount DECIMAL(10,2) NOT NULL,
    ValidUntil DATE NOT NULL,
    Status NVARCHAR(10) NOT NULL DEFAULT 'PEND',
    LastUpdatedDate DATE NOT NULL,
    CreatedDate datetime2(7) NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy nvarchar(100) NOT NULL DEFAULT 'System',
    ModifiedDate datetime2(7) NULL,
    ModifiedBy nvarchar(100) NULL,
    FOREIGN KEY (Status) REFERENCES WF_QuoteStatus (StatusCode),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

-- Quote Items Table
CREATE TABLE WF_QuoteItems (
    QuoteItemID INT IDENTITY(1,1) PRIMARY KEY,
    QuoteID INT NOT NULL,
    Description NVARCHAR(500) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL, -- Rule.sum(quoteItems)
    SortOrder INT NOT NULL DEFAULT 1,
    FOREIGN KEY (QuoteID) REFERENCES WF_Quotes(QuoteID)
);

CREATE TABLE WF_FileTypes(
    FileType NVARCHAR(5) PRIMARY KEY,
    FileTypeName NVARCHAR(100) NOT NULL
);

INSERT INTO WF_FileTypes (FileType, FileTypeName) VALUES
('APP', 'Application'),
('ING', 'Ingredients'),
('PROD', 'Products'),
('OTHER', 'Other');

-- Files Table
CREATE TABLE WF_Files (
    FileID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    FileName NVARCHAR(500) NOT NULL,
    FileType NVARCHAR(5) NOT NULL,
    FileSize NVARCHAR(20) NULL,
    UploadedDate DATE NOT NULL,
    Tag NVARCHAR(200) NULL,
    IsProcessed BIT NOT NULL DEFAULT 0,
    RecordCount INT NULL,
    FilePath NVARCHAR(1000) NULL,
    CCreatedDate datetime2(7) NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy nvarchar(100) NOT NULL DEFAULT 'System',
    ModifiedDate datetime2(7) NULL,
    ModifiedBy nvarchar(100) NULL,
    FOREIGN KEY (FileType) REFERENCES WF_FileTypes(FileType),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

-- Messages Table
CREATE TABLE WF_ApplicationMessages (
    MessageID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    FromUser NVARCHAR(200) NOT NULL,
    ToUser NVARCHAR(200) NOT NULL,
    MessageText NVARCHAR(MAX) NOT NULL,
    MessageType NVARCHAR(50) NOT NULL DEFAULT 'outgoing',
    Priority NVARCHAR(20) NOT NULL DEFAULT 'normal',
    SentDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

-- Comments Table
CREATE TABLE WF_ApplicationComments (
    CommentID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    Author NVARCHAR(200) NOT NULL,
    CommentText NVARCHAR(MAX) NOT NULL,
    CommentType NVARCHAR(50) NOT NULL DEFAULT 'internal',
    Category NVARCHAR(100) NULL,
    CreatedDate datetime2(7) NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy nvarchar(100) NOT NULL DEFAULT 'System',
    ModifiedDate datetime2(7) NULL,
    ModifiedBy nvarchar(100) NULL,
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

CREATE TABLE WF_ActivityStatus(
	StatusCode NVARCHAR(5) NOT NULL PRIMARY KEY,
	StatusDesc NVARCHAR(50)
);

INSERT INTO WF_ActivityStatus (StatusCode, StatusDesc) VALUES
('APP','Approved'),
('REJ','Rejected');


-- Activity Log Table
CREATE TABLE WF_ActivityLog (
    ActivityID INT IDENTITY(1,1) PRIMARY KEY,
    ApplicationID INT NOT NULL,
    ActionType NVARCHAR(200) NOT NULL,
    ActionDetails NVARCHAR(MAX) NULL,
    UserName NVARCHAR(200) NOT NULL,
    ActivityType NVARCHAR(100) NOT NULL,
    Status NVARCHAR(5) NOT NULL DEFAULT 'APP',
    Category NVARCHAR(100) NULL,
    ActivityDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (Status) REFERENCES WF_ActivityStatus (StatusCode),
    FOREIGN KEY (ApplicationID) REFERENCES WF_Applications(ApplicationID)
);

-- =============================================
-- CREATE INDEXES
-- =============================================

-- Performance indexes
CREATE INDEX IX_WF_Applications_CompanyID ON WF_Applications(CompanyID);
CREATE INDEX IX_WF_Applications_Status ON WF_Applications(Status);
CREATE INDEX IX_WF_Applications_ApplicationNumber ON WF_Applications(ApplicationNumber);
CREATE INDEX IX_ValidationChecks_ApplicationID ON WF_Applications(ApplicationID);
CREATE INDEX IX_Plants_ApplicationID ON WF_Plants(ApplicationID);
CREATE INDEX IX_Products_ApplicationID ON WF_Products(ApplicationID);
CREATE INDEX IX_Ingredients_ApplicationID ON WF_Ingredients(ApplicationID);
--CREATE INDEX IX_Ingredients_NCRCIngredientID ON WF_Ingredients(NCRCIngredientID);
CREATE INDEX IX_Quotes_ApplicationID ON WF_Quotes(ApplicationID);
CREATE INDEX IX_Files_ApplicationID ON WF_Files(ApplicationID);
CREATE INDEX IX_Messages_ApplicationID ON WF_ApplicationMessages(ApplicationID);
CREATE INDEX IX_Comments_ApplicationID ON WF_ApplicationComments(ApplicationID);
CREATE INDEX IX_ActivityLog_ApplicationID ON WF_ActivityLog(ApplicationID);
CREATE INDEX IX_ActivityLog_ActivityDate ON WF_ActivityLog(ActivityDate);

-- =============================================
-- INSERT SAMPLE DATA
-- =============================================

-- Insert Users
INSERT INTO WF_Users (Username, FullName, Email, Role) VALUES
('jmitchell', 'John Mitchell', 'john@happycowmills.com', 'ADMIN'),
('gmagder', 'Gary Magder', 'gmagder@happycowmills.com', 'RFR'),
('system', 'System Import', 'system@ncrc.com', 'ADMIN'),
('autosync', 'Auto-Sync', 'autosync@ncrc.com', 'NCRC');



-- Insert Application
INSERT INTO WF_Applications (
    ApplicationNumber, CompanyID, SubmissionDate, Status
) VALUES (
    9999, 1, '2025-07-17', 'NEW'
);



-- Insert mock data into WF_Products
INSERT INTO [dbo].[WF_Products] (
    [ApplicationID],
    [action],
    [legacyId],
    [doNotImport],
    [message],
    [labelType],
    [labelName],
    [brandName],
    [labelCompanyId],
    [distributorName],
    [group],
    [symbol],
    [dpm],
    [category],
    [usePlantStatus],
    [status],
    [legacyStatus],
    [consumer],
    [industrial],
    [finalized],
    [processedBy],
    [processedDate],
    [notes]
) VALUES
    (1, 'Add', '1142395', 0, NULL, 'In-House', 'Product ABC', 'Hungry Jack ®', '2584', 'Basic American Foods', '3', 'OU', 'Pareve', 'Potato Products', 0, 'pending', NULL, 0, 0, 0, 'Excel Import', '2025-08-20', 'Imported from Book 9.xlsx'),
    (1, 'Add', '1142396', 0, NULL, 'In-House', 'Product XYZ', 'Fresh Farms', '2585', 'Fresh Produce Inc.', '3', 'OU', 'Dairy', 'Vegetable Blends', 0, 'pending', NULL, 0, 0, 0, 'Excel Import', '2025-08-20', 'Imported from Book 9.xlsx'),
    (1, 'Add', '1142397', 0, NULL, 'Private', 'Snack Mix A', 'Crunchy Time', '2586', 'National Snack Co.', '3', 'OU', 'Pareve', 'Snack Foods', 0, 'pending', NULL, 0, 0, 0, 'Excel Import', '2025-08-20', 'Imported from Book 9.xlsx'),
    (1, 'Add', '1142398', 0, NULL, 'In-House', 'Soup Base Z', 'Gourmet Chefs', '2587', 'Culinary Distributors LLC', '3', 'OU', 'Meat', 'Soup Bases', 0, 'pending', NULL, 0, 0, 0, 'Excel Import', '2025-08-20', 'Imported from Book 9.xlsx');



-- Insert mock data
INSERT INTO WF_Ingredients (ApplicationID,
    Source, UKDId, RMC, IngredientName, Manufacturer, Brand, 
    Packaging, Agency, AddedDate, AddedBy, Status, NCRCId
)
VALUES 
    (1,'File 1', NULL, NULL, 'Ryman Rye Grain', 'Jones Farms Organics', 'Jones Farms Organics', 
     'bulk', 'OU', '2025-07-17', 'System Import', 'Original', 'ING-2025-1001'),
    
    (1,'File 1', NULL, NULL, 'Yecora Rojo Grain', 'Jones Farms Organics', 'Jones Farms Organics', 
     'bulk', 'OU', '2025-07-17', 'System Import', 'Original', 'ING-2025-1002'),
    
    (1,'File 2', NULL, NULL, 'Durham Grain', 'cow & Livestock', 'cow & Livestock', 
     'bulk', 'OU', '2025-07-17', 'System Import', 'Original', 'ING-2025-1003'),
    
    (1,'File 2', NULL, NULL, 'Purple Barley Grain', 'cow & Livestock', 'cow & Livestock', 
     'bulk', 'OU', '2025-07-17', 'System Import', 'Original', 'ING-2025-1004'),
    
    (1,'File 2', NULL, NULL, 'Emmer Grain', 'cow Farms', 'cow Farms', 
     'bulk', 'OU', '2025-07-17', 'System Import', 'Original', 'ING-2025-1005'),
    
    (1,'File 2', NULL, NULL, 'Einkorn Grain', 'cow Farms', 'cow Farms', 
     'bulk', 'OU', '2025-07-17', 'System Import', 'Original', 'ING-2025-1006'),
    
    (1,'File 2', NULL, NULL, 'Spelt Grain', 'cow Farms', 'cow Farms', 
     'bulk', 'OU', '2025-07-17', 'System Import', 'Original', 'ING-2025-1007'),
    
    (1,'Manual Entry', 'OUE9-VAN2024', NULL, 'Natural Vanilla Extract', 'Premium Flavor Co', 'Premium Flavor Co', 
     'Packaged', 'OU', '2025-07-18', 'J. Mitchell', 'Recent', 'ING-2025-1008'),
    
    (1,'Manual Entry', NULL, NULL, 'Organic Quinoa Flour', 'Andean Grains Ltd', 'Andean Grains', 
     'bulk', 'OU-P', '2025-07-18', 'G. Magder', 'Recent', 'ING-2025-1009'),
    
    (1,'Supplier Update', NULL, NULL, 'Coconut Oil (Refined)', 'Tropical Oils Inc', 'TropicalPure', 
     'Packaged', 'OU', '2025-07-18', 'Auto-Sync', 'Recent', 'ING-2025-1010');

    -- -- Insert Company
    -- INSERT INTO Companies (
    --     KashrusCompanyID, ApplicationID, CompanyName, Category, CurrentlyCertified, EverCertified,
    --     StreetAddress, AddressLine2, City, State, Country, ZipCode, Website,
    --     OwnBrand, CopackerDirectory, VeganCertification, PlantCount
    -- ) VALUES (
    --     'KC-2025-4829', 1, 'Happy Cow Mills Inc.', 'Pharmaceutical / Nutraceutical', 0, 0,
    --     '1250 Industrial Parkway', 'Building A, Suite 100', 'Rochester', 'NY', 'USA', '14624', 'www.happycowmills.com',
    --     1, 1, 1, 1
    -- );
    -- -- Insert Validation Checks
    -- INSERT INTO ValidationChecks (ApplicationID, CheckType, IsValid, ValidationMessage) VALUES
    -- (1, 'company', 1, 'Company KC-2025-4829 verified in Kashrus DB'),
    -- (1, 'plant', 1, 'Plant PLT-KC-2025-4829-001 created and linked'),
    -- (1, 'contacts', 1, 'Primary contact John Mitchell designated for initial communication'),
    -- (1, 'products', 1, '4 products identified and categorized'),
    -- (1, 'ingredients', 1, '10 ingredients processed and validated'),
    -- (1, 'quote', 0, 'Quote not found - needs verification'),
    -- (1, 'documentation', 1, 'All required documents uploaded and processed');

    -- -- Insert Contacts
    -- INSERT INTO Contacts (ApplicationID, ContactType, FullName, JobTitle, Phone, Email, IsPrimary, Role) VALUES
    -- (1, 'Primary Contact', 'John Mitchell', NULL, '9176966517', 'john@happycowmills.com', 1, 'primary_communication'),
    -- (1, 'Additional Contact', 'Gary Magder', 'Quality Assurance Manager', '9176966517', 'gmagder@happycowmills.com', 0, 'technical_contact');

    -- -- Insert Plant
    -- INSERT INTO Plants (
    --     ApplicationID, PlantNumber, PlantName, StreetAddress, AddressLine2, City, State, Country, Province, Region, ZipCode,
    --     ContactName, ContactTitle, ContactPhone, ContactEmail, ManufacturingProcess, ClosestMajorCity,
    --     HasOtherProducts, OtherProductsList, HasOtherPlants, OtherPlantsLocation,
    --     OperationalStatus, LastInspection, ComplianceStatus
    -- ) VALUES (
    --     1, 'PLT-KC-2025-4829-001', 'Happy Cow Mills Production Facility',
    --     '1250 Industrial Parkway', 'Building A, Suite 100', 'Rochester', 'NY', 'USA', 'N/A', 'Western New York', '14624',
    --     'John Mitchell', 'Plant Manager', '(585) 555-0123', 'j.mitchell@happycowmills.com',
    --     'Grain cleaning, milling, and flour production. Raw grains are received in bulk, cleaned using mechanical separators, ground using stone mills, sifted through mesh screens, and packaged in food-grade containers. All processes follow HACCP guidelines.',
    --     'Rochester, NY (15 miles)', 1, 'Animal feed supplements, grain storage services', 1, 'Secondary facility at 425a Commerce Drive, Rochester NY',
    --     'Active', 'Pending', 'Under Review'
    -- );

    -- -- Insert Products
    -- INSERT INTO Products (ApplicationID, Source, LabelName, BrandName, LabelCompany, ConsumerIndustrial, BulkShipped, CertificationSymbol, Status, Category) VALUES
    -- (1, 'Brands File 1', 'Yecora Rojo Flour', 'cow Mill', 'cow Mill', 'C', 'Y', 'OU', 'submitted', 'flour'),
    -- (1, 'Brands File 1', 'Rye Flour', 'cow Mill', 'cow Mill', 'C', 'Y', 'OU', 'submitted', 'flour'),
    -- (1, 'Form Data', 'cheese man', 'cheesy', 'Happy Cow Mills', 'C', 'Y', 'OU', 'submitted', 'cheese'),
    -- (1, 'Form Data', 'cheese chocolate', 'choccheese', 'Happy Cow Mills', 'C', 'Y', 'OU', 'submitted', 'cheese');

    -- -- Insert Ingredients
    -- INSERT INTO Ingredients (ApplicationID, NCRCIngredientID, Source, UKDID, RMC, IngredientName, Manufacturer, Brand, Packaging, CertificationAgency, AddedDate, AddedBy, Status) VALUES
    -- (1, 'ING-2025-1001', 'File 1', '', '', 'Ryman Rye Grain', 'Jones Farms Organics', 'Jones Farms Organics', 'bulk', 'OU', '2025-07-17', 'System Import', 'Original'),
    -- (1, 'ING-2025-1002', 'File 1', '', '', 'Yecora Rojo Grain', 'Jones Farms Organics', 'Jones Farms Organics', 'bulk', 'OU', '2025-07-17', 'System Import', 'Original'),
    -- (1, 'ING-2025-1003', 'File 2', '', '', 'Durham Grain', 'cow & Livestock', 'cow & Livestock', 'bulk', 'OU', '2025-07-17', 'System Import', 'Original'),
    -- (1, 'ING-2025-1004', 'File 2', '', '', 'Purple Barley Grain', 'cow & Livestock', 'cow & Livestock', 'bulk', 'OU', '2025-07-17', 'System Import', 'Original'),
    -- (1, 'ING-2025-1005', 'File 2', '', '', 'Emmer Grain', 'cow Farms', 'cow Farms', 'bulk', 'OU', '2025-07-17', 'System Import', 'Original'),
    -- (1, 'ING-2025-1006', 'File 2', '', '', 'Einkorn Grain', 'cow Farms', 'cow Farms', 'bulk', 'OU', '2025-07-17', 'System Import', 'Original'),
    -- (1, 'ING-2025-1007', 'File 2', '', '', 'Spelt Grain', 'cow Farms', 'cow Farms', 'bulk', 'OU', '2025-07-17', 'System Import', 'Original'),
    -- (1, 'ING-2025-1008', 'Manual Entry', 'OUE9-VAN2024', '', 'Natural Vanilla Extract', 'Premium Flavor Co', 'Premium Flavor Co', 'Packaged', 'OU', '2025-07-18', 'J. Mitchell', 'Recent'),
    -- (1, 'ING-2025-1009', 'Manual Entry', '', '', 'Organic Quinoa Flour', 'Andean Grains Ltd', 'Andean Grains', 'bulk', 'OU-P', '2025-07-18', 'G. Magder', 'Recent'),
    -- (1, 'ING-2025-1010', 'Supplier Update', '', '', 'Coconut Oil (Refined)', 'Tropical Oils Inc', 'TropicalPure', 'Packaged', 'OU', '2025-07-18', 'Auto-Sync', 'Recent');

-- Insert Quote
INSERT INTO WF_Quotes (ApplicationID, QuoteNumber, TotalAmount, ValidUntil, Status, LastUpdatedDate) VALUES
(1, 'QT-2025-HC-001', 2850.00, '2025-08-17', 'PEND', '2025-07-17');

-- Insert Quote Items
INSERT INTO WF_QuoteItems (QuoteID, Description, Amount, SortOrder) VALUES
(1, 'Initial Certification - 1 Plant', 1500.00, 1),
(1, 'Product Review (4 products)', 800.00, 2),
(1, 'Ingredient Analysis (10 ingredients)', 550.00, 3);

-- Insert Files
INSERT INTO WF_Files (ApplicationID, FileName, FileType, FileSize, UploadedDate, Tag, IsProcessed, RecordCount) VALUES
(1, 'Application for OU Kosher Certification - Test.pdf', 'APP', '245 KB', '2025-07-17', 'Application Form', 1, NULL),
(1, 'happycow IngredientOUKosher.xlsx', 'ING', '12 KB', '2025-07-17', 'Ingredient List', 1, 2),
(1, 'happycow BrandsOUKosher.xlsx', 'PROD', '8 KB', '2025-07-17', 'Brand/Product List', 1, 2),
(1, 'Ingredient happycowOUKosher 1.xlsx', 'ING', '15 KB', '2025-07-17', 'Ingredient List (Additional)', 1, 5),
(1, 'happycow BrandsOUKosher 1.xlsx', 'PROD', '9 KB', '2025-07-17', 'Brand/Product List (Additional)', 1, 2),
(1, 'Screen List Matrix VR2Screens.csv', 'OTHER', '3 KB', '2025-07-17', 'Reference Data', 1, NULL);

-- Insert Messages
---NSERT INTO WF_Messages (ApplicationID, FromUser, ToUser, MessageText, MessageType, Priority, SentDate) VALUES
--(1, 'J. Mitchell', 'Dispatcher', 'Application ready for initial review. All documentation complete.', 'outgoing', 'normal', '2025-07-18 09:30:00');

-- Insert Comments
--INSERT INTO WF_Comments (ApplicationID, Author, CommentText, CommentType, Category, CreatedDate) VALUES
--(1, 'J. Mitchell', 'Verified all ingredient certifications with suppliers. Coconut oil documentation updated.', 'internal', 'verification', '2025-07-18 14:45:00'),
--(1, 'G. Magder', 'Plant contact information confirmed. John Mitchell will be primary for all communications.', 'internal', 'contact_management', '2025-07-18 13:20:00');

-- Insert Activity Log
INSERT INTO WF_ActivityLog (ApplicationID, ActionType, ActionDetails, UserName, ActivityType, Status, Category, ActivityDate) VALUES
(1, 'Ingredient Added', 'Natural Vanilla Extract (Premium Flavor Co)', 'J. Mitchell', 'ingredient', 'APP', 'data_entry', '2025-07-18 14:30:00'),
(1, 'Ingredient Added', 'Organic Quinoa Flour (Andean Grains Ltd)', 'G. Magder', 'ingredient', 'APP', 'data_entry', '2025-07-18 13:15:00'),
(1, 'Supplier Sync', 'Coconut Oil (Refined) auto-added from supplier portal', 'Auto-Sync', 'ingredient', 'APP', 'automation', '2025-07-18 11:45:00'),
(1, 'Plant Updated', 'Manufacturing process description revised', 'J. Mitchell', 'plant', 'APP', 'information_update', '2025-07-18 09:20:00'),
(1, 'Initial Import', '7 ingredients imported from application submission', 'System Import', 'bulk', 'APP', 'bulk_import', '2025-07-17 16:45:00'),
(1, 'Company Created', 'Happy Cow Mills Inc. added to Kashrus DB (KC-2025-4829)', 'System', 'company', 'APP', 'company_setup', '2025-07-17 16:30:00');

-- =============================================
-- VERIFY DATA WITH SAMPLE QUERIES
-- =============================================

-- Application Overview
SELECT 
    a.ApplicationNumber,
    a.Status,
    COUNT(DISTINCT p.ProductID) as ProductCount,
    COUNT(DISTINCT i.IngredientID) as IngredientCount,
    COUNT(DISTINCT f.FileID) as FileCount
FROM WF_Applications a
INNER JOIN WF_Companies c ON a.CompanyID = c.CompanyID
LEFT JOIN WF_Products p ON a.ApplicationID = p.ApplicationID
LEFT JOIN WF_Ingredients i ON a.ApplicationID = i.ApplicationID
LEFT JOIN WF_Files f ON a.ApplicationID = f.ApplicationID
WHERE a.ApplicationNumber = 1
GROUP BY a.ApplicationNumber, a.Status;


-- Recent Activity (last 7 days)
SELECT 
    ActivityDate,
    ActionType,
    ActionDetails,
    UserName,
    Status
FROM WF_ActivityLog 
WHERE ApplicationID = 1 
AND ActivityDate >= DATEADD(day, -7, GETDATE())
ORDER BY ActivityDate DESC;


-- Files Processing Status
SELECT 
    FileType,
    COUNT(*) as TotalFiles,
    SUM(CASE WHEN IsProcessed = 1 THEN 1 ELSE 0 END) as ProcessedFiles,
    SUM(ISNULL(RecordCount, 0)) as TotalRecords
FROM WF_Files 
WHERE ApplicationID = 1
GROUP BY FileType;