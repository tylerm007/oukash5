 use dashboardv1;

-- Drop child tables first (tables with foreign keys)
DROP TABLE IF EXISTS SubmissionRequest;
DROP TABLE IF EXISTS SubmissionRawData;
DROP TABLE IF EXISTS SubmissionIngredients;
DROP TABLE IF EXISTS SubmissionProducts;
DROP TABLE IF EXISTS SubmissionFiles;
DROP TABLE IF EXISTS SubmissionFileLinks;
DROP TABLE IF EXISTS SubmissionPlant;
DROP TABLE IF EXISTS SubmissionCompany;

-- This is the Company Application Table
CREATE TABLE SubmissionCompany (
    SubmissionFormId [int] IDENTITY(1,1) NOT NULL,
    submission_id  [nvarchar](50),
    submission_date DATETIME DEFAULT GETDATE(),
    OUcertified BIT DEFAULT 0, -- "Are you currently certified by the OU?"
    everCertified BIT DEFAULT 0, -- "Have you ever been certified by the OU?"
    agencyName  [nvarchar](50), -- If yes, please provide the name of the certifying agency.
    companyName  [nvarchar](50), --Company Name
    companyAddress  [nvarchar](100), -- Company Street Address street1
    companyAddress2 [nvarchar](100), -- Company Street Address street2
    companyCity  [nvarchar](50),
    companyCountry  [nvarchar](10),
    companyState [nvarchar](25), -- Company State
    companyRegion  [nvarchar](50),
    companyProvince  [nvarchar](50),
    companyPhone  [nvarchar](250),
    ZipPostalCode  [nvarchar](15),
    companyWebsite  [nvarchar](250),
    IsPrimaryContact BIT DEFAULT 1,
    contactFirst  [nvarchar](100), --Company Contact First Name
    contactLast  [nvarchar](100), --Company Contact Last Name
    contactPhone  [nvarchar](25), -- Company Contact Phone
    contactEmail  [nvarchar](100), -- Company Contact Email Address
    billingContact  [nvarchar](250), --Billing Contact (person receiving invoices)
    billingContactFirst  [nvarchar](100), -- Billing Company Contact First Name
    billingContactLast  [nvarchar](100), --Billing Company Contact Last Name
    billingContactPhone  [nvarchar](25), -- Billing Company Contact Phone
    billingContactEmail  [nvarchar](100), -- Billing Company Contact Email Address
    jobTitle [nvarchar](100),
    contactFirst1  [nvarchar](100), --Alt Company Contact First Name
    contactLast1  [nvarchar](100), --Alt Company Contact Last Name
    contactPhone1  [nvarchar](25), -- Alt Company Contact Phone
    contactEmail1  [nvarchar](100), -- Alt Company Contact Email Address
    jobTitle1 [nvarchar](100),
    whatWould [text], -- "What would you like to certify?"
    whichCategory  [nvarchar](50), -- "Which category would your product(s) fall under?
    whereDidHear  [nvarchar](50), -- "Where did you hear about OU Kosher?
    pleaseSpecify  [text], -- 
    copack  [nvarchar](10), -- Are you producing a product under your own brand, as a Copacker for another company, or both?
    listInCopack [BIT] default 0,
    veganCert BIT DEFAULT 0, -- Would you like an ISO accredited vegan certification for any of these products?
    areThere BIT DEFAULT 0,-- "Are there additional contacts?
    numberOfPlants [int]  DEFAULT 1, -- Number of Plants in this Application,
    formName  [nvarchar](250),
    language [nvarchar](50),
    status [nvarchar](50) DEFAULT 'New',
    kashrusLink  [nvarchar](250),
    submissionurl  [nvarchar](250),
    PRIMARY KEY CLUSTERED 
(
	[SubmissionFormId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
    
-- Application can have 1:M Plants
-- typeA ['Plant location information is the same as company location information above.']"
-- 
CREATE TABLE SubmissionPlant (
    PlantId [int] IDENTITY(1,1) NOT NULL,  
    plantNumber [int] NOT NULL,
    SubmissionFormId [int]  NOT NULL, 
    plantName  [nvarchar](250), 
    plantAddress  [nvarchar](100),
    plantCity  [nvarchar](50),
    plantState  [nvarchar](250), -- Plant Region
    plantZip  [nvarchar](50),
    plantCountry  [nvarchar](10),
    plantRegion  [nvarchar](50),   
    plantProvince  [nvarchar](50),
    contactFirst  [nvarchar](100), --Company Contact First Name
    contactLast  [nvarchar](100), --Company Contact Last Name
    contactPhone  [nvarchar](25), -- Company Contact Phone
    contactEmail  [nvarchar](100), -- Company Contact Email Address
    jobTitle [nvarchar](100),

    contactFirst1  [nvarchar](100), --Alt -Company Contact First Name
    contactLast1  [nvarchar](100), --Company Contact Last Name
    contactPhone1  [nvarchar](25), -- Company Contact Phone
    contactEmail1  [nvarchar](100), -- Company Contact Email Address
    jobTitle1 [nvarchar](100),

    majorCity [nvarchar](100),  --If the facility is not located in a major city, please indicate the closest major city and distance
    brieflySummarize TEXT, -- "Please briefly summarize the operations taking place at this facility."
    productDesc TEXT, --"Please briefly list the products that are not part of this application but are being produced in the same plant."
    otherProducts BIT DEFAULT 1,  --"Are any other products produced in this plant?
    areAny BIT DEFAULT 0, --"Are any of these products also produced in a plant not included in this application"
    otherProductCompany TEXT, -- "If yes, please list the other companies that produce products in this plant."
    FOREIGN KEY (SubmissionFormId) REFERENCES SubmissionCompany(SubmissionFormId),
    PRIMARY KEY CLUSTERED 
(
	[PlantId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

    
CREATE TABLE SubmissionFileLinks(
    FileLinkId [int] IDENTITY(1,1) NOT NULL,   
    SubmissionFormId [int]  NOT NULL,
    productFileURL  [nvarchar](250),
    ingredientURL  [nvarchar](250), -- Ingredient Statement File
    productFileURL1  [nvarchar](250), -- Product Label File
    ingredientURL1  [nvarchar](250), -- Ingredient List File
    productFileURL2  [nvarchar](250), --Product Specification File
    ingredientURL2  [nvarchar](250), -- Ingredient Declaration File
    productFileURL3  [nvarchar](250),  -- Product Photos File
    ingredientURL3  [nvarchar](250),  -- Ingredient Sourcing File
    productFileURL4  [nvarchar](250), -- Product Formulation File
    ingredientURL4  [nvarchar](250), -- Ingredient Sourcing File
    
    FOREIGN KEY (SubmissionFormId) REFERENCES SubmissionCompany(SubmissionFormId),
    PRIMARY KEY CLUSTERED 
(
	[FileLinkId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


-- suggestted mapping S3
CREATE TABLE SubmissionFiles(
    JotFormFileId [int] IDENTITY(1,1) NOT NULL,   
    SubmissionFormId [int]  NOT NULL,
    fileName  [nvarchar](250),
    fileLURL  [nvarchar](250),
    fileType  [nvarchar](6),
    fileSize [int] ,
    Content [TEXT],
    uploadDate DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (SubmissionFormId) REFERENCES SubmissionCompany(SubmissionFormId),
    PRIMARY KEY CLUSTERED 
(
	[JotFormFileId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

-- typeA78 == 'Enter manually'
-- typeA80 returns [{}] 
-- {"Product Name":"Bagel","Retail?":"Y","Industrial?":"N","Brand Name":"None","In-house?":"Y","Private Label?":"No","Private Label Co":"No"}
CREATE TABLE SubmissionProducts(
    SubmissionProductId [int] IDENTITY(1,1) NOT NULL,
    SubmissionPlantId [int]  NOT NULL,
    productName [nvarchar](250),
    Retail BIT DEFAULT 1,
    Industrial BIT DEFAULT 0,
    BrandName [nvarchar](250),
    inHouse BIT DEFAULT 1,
    privateLabel BIT DEFAULT 0,
    privateLabelCo [nvarchar](250),
    
    FOREIGN KEY (JotPlantId) REFERENCES SubmissionPlant(PlantId),
    PRIMARY KEY CLUSTERED 
(
	[SubmissionProductId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

-- selectPreferred == 'Enter manually'
-- name == Enter returns [{}]
--  {"UKD-ID":"0","Raw Material Code":"Flour","Ingredient Label Name":"Flour","Manufacturer":"local","Brand Name":"Flour","Packaged/Bulk":"Bulk","Certifying Agency":"OU"}
CREATE TABLE SubmissionIngredients(
    SubmissionIngredientId [int] IDENTITY(1,1) NOT NULL,
    SubmissionPlantId [int]  NOT NULL, 
    UKDID [nvarchar](50), 
    rawMaterialCode [nvarchar](50),
    ingredientLabelName [nvarchar](100),
    manufacturer [nvarchar](100),
    brandName [nvarchar](100),
    packagedOrBulk [nvarchar](15),
    certifyingAgency [nvarchar](25),

    FOREIGN KEY (JotPlantId) REFERENCES SubmissionPlant(PlantId),
    PRIMARY KEY CLUSTERED 
(
	[SubmissionIngredientId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE SubmissionRawData (
    SubmissionRawDataId [int] IDENTITY(1,1) NOT NULL,  
    SubmissionFormId [int]  NOT NULL,
    entryorder [int] NOT NULL,
    prompt [nvarchar](250),
    name [nvarchar](250),
    control_type [nvarchar](50),
    answer TEXT,
   FOREIGN KEY (SubmissionFormId) REFERENCES SubmissionCompany(SubmissionFormId),
    PRIMARY KEY CLUSTERED 
(
	[SubmissionRawDataId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

CREATE TABLE SubmissionRequest (
    SubmissionRequestId INT IDENTITY(1,1) PRIMARY KEY,
    SubmissionAppId INT NOT NULL,
    SubmissionStatus NVARCHAR(50) NOT NULL DEFAULT 'NEW', -- NEW, IN_PROGRESS, COMPLETED, FAILED
    SubmissionType NVARCHAR(50) NOT NULL, -- e.g., 'Initial Review', 'Follow-up', etc.
    ApplicationId NVARCHAR(255) NULL,
    SubmissionMessage TEXT NULL,
    created_date DATETIME2 DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME2 NULL,
    FOREIGN KEY (SubmissionAppId) REFERENCES SubmissionApplication(SubmissionAppId)
);
GO