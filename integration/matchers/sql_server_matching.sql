-- =============================================================================
-- Company/Plant Fuzzy Matching - SQL Server Implementation
-- =============================================================================
-- 
-- This provides a pure T-SQL implementation for environments where Python
-- is not available. Uses standardization + Levenshtein distance + scoring.
--
-- =============================================================================

USE [KosherCertification]
GO

-- -----------------------------------------------------------------------------
-- HELPER FUNCTIONS
-- -----------------------------------------------------------------------------

-- Levenshtein Distance Function
CREATE OR ALTER FUNCTION dbo.fn_LevenshteinDistance (
    @s1 NVARCHAR(255),
    @s2 NVARCHAR(255)
)
RETURNS INT
AS
BEGIN
    DECLARE @s1_len INT = LEN(ISNULL(@s1, ''))
    DECLARE @s2_len INT = LEN(ISNULL(@s2, ''))
    
    IF @s1_len = 0 RETURN @s2_len
    IF @s2_len = 0 RETURN @s1_len
    
    -- Use iterative approach with table variable
    DECLARE @d TABLE (i INT, j INT, cost INT, PRIMARY KEY (i, j))
    DECLARE @i INT, @j INT, @cost INT
    DECLARE @s1_char NCHAR(1), @s2_char NCHAR(1)
    
    -- Initialize first column
    SET @i = 0
    WHILE @i <= @s1_len
    BEGIN
        INSERT INTO @d (i, j, cost) VALUES (@i, 0, @i)
        SET @i = @i + 1
    END
    
    -- Initialize first row
    SET @j = 1
    WHILE @j <= @s2_len
    BEGIN
        INSERT INTO @d (i, j, cost) VALUES (0, @j, @j)
        SET @j = @j + 1
    END
    
    -- Fill in the rest
    SET @i = 1
    WHILE @i <= @s1_len
    BEGIN
        SET @s1_char = SUBSTRING(@s1, @i, 1)
        SET @j = 1
        WHILE @j <= @s2_len
        BEGIN
            SET @s2_char = SUBSTRING(@s2, @j, 1)
            SET @cost = CASE WHEN @s1_char = @s2_char THEN 0 ELSE 1 END
            
            INSERT INTO @d (i, j, cost)
            SELECT @i, @j, MIN(cost)
            FROM (
                SELECT (SELECT cost FROM @d WHERE i = @i - 1 AND j = @j) + 1 AS cost
                UNION ALL
                SELECT (SELECT cost FROM @d WHERE i = @i AND j = @j - 1) + 1
                UNION ALL
                SELECT (SELECT cost FROM @d WHERE i = @i - 1 AND j = @j - 1) + @cost
            ) AS costs
            
            SET @j = @j + 1
        END
        SET @i = @i + 1
    END
    
    RETURN (SELECT cost FROM @d WHERE i = @s1_len AND j = @s2_len)
END
GO


-- String Similarity (0-100 scale based on Levenshtein)
CREATE OR ALTER FUNCTION dbo.fn_StringSimilarity (
    @s1 NVARCHAR(255),
    @s2 NVARCHAR(255)
)
RETURNS DECIMAL(5,2)
AS
BEGIN
    DECLARE @maxLen INT = CASE 
        WHEN LEN(ISNULL(@s1, '')) > LEN(ISNULL(@s2, '')) THEN LEN(@s1)
        ELSE LEN(ISNULL(@s2, ''))
    END
    
    IF @maxLen = 0 RETURN 100.0
    
    DECLARE @distance INT = dbo.fn_LevenshteinDistance(@s1, @s2)
    
    RETURN (1.0 - (CAST(@distance AS DECIMAL) / @maxLen)) * 100
END
GO


-- Standardize Company Name
CREATE OR ALTER FUNCTION dbo.fn_StandardizeCompanyName (
    @name NVARCHAR(255)
)
RETURNS NVARCHAR(255)
AS
BEGIN
    IF @name IS NULL RETURN ''
    
    DECLARE @result NVARCHAR(255) = UPPER(LTRIM(RTRIM(@name)))
    
    -- Remove common suffixes (order matters - longer first)
    SET @result = REPLACE(@result, ' INCORPORATED', '')
    SET @result = REPLACE(@result, ' CORPORATION', '')
    SET @result = REPLACE(@result, ' LIMITED', '')
    SET @result = REPLACE(@result, ' COMPANY', '')
    SET @result = REPLACE(@result, ' L.L.C.', '')
    SET @result = REPLACE(@result, ' INC.', '')
    SET @result = REPLACE(@result, ' INC', '')
    SET @result = REPLACE(@result, ' LLC.', '')
    SET @result = REPLACE(@result, ' LLC', '')
    SET @result = REPLACE(@result, ' LTD.', '')
    SET @result = REPLACE(@result, ' LTD', '')
    SET @result = REPLACE(@result, ' CORP.', '')
    SET @result = REPLACE(@result, ' CORP', '')
    SET @result = REPLACE(@result, ' CO.', '')
    SET @result = REPLACE(@result, ' CO', '')
    
    -- Standardize common words
    SET @result = REPLACE(@result, ' MANUFACTURING', ' MFG')
    SET @result = REPLACE(@result, ' INTERNATIONAL', ' INTL')
    SET @result = REPLACE(@result, ' INDUSTRIES', ' IND')
    SET @result = REPLACE(@result, ' ENTERPRISES', ' ENT')
    SET @result = REPLACE(@result, ' PRODUCTS', ' PROD')
    SET @result = REPLACE(@result, ' TECHNOLOGIES', ' TECH')
    SET @result = REPLACE(@result, ' BROTHERS', ' BROS')
    SET @result = REPLACE(@result, '&', ' AND ')
    
    -- Remove punctuation
    SET @result = REPLACE(@result, ',', '')
    SET @result = REPLACE(@result, '.', '')
    SET @result = REPLACE(@result, '''', '')
    SET @result = REPLACE(@result, '"', '')
    SET @result = REPLACE(@result, '-', ' ')
    
    -- Normalize whitespace
    WHILE CHARINDEX('  ', @result) > 0
        SET @result = REPLACE(@result, '  ', ' ')
    
    RETURN LTRIM(RTRIM(@result))
END
GO


-- Standardize Street Address
CREATE OR ALTER FUNCTION dbo.fn_StandardizeStreet (
    @street NVARCHAR(255)
)
RETURNS NVARCHAR(255)
AS
BEGIN
    IF @street IS NULL RETURN ''
    
    DECLARE @result NVARCHAR(255) = UPPER(LTRIM(RTRIM(@street)))
    
    -- Street types
    SET @result = REPLACE(@result, ' STREET', ' ST')
    SET @result = REPLACE(@result, ' AVENUE', ' AVE')
    SET @result = REPLACE(@result, ' BOULEVARD', ' BLVD')
    SET @result = REPLACE(@result, ' DRIVE', ' DR')
    SET @result = REPLACE(@result, ' ROAD', ' RD')
    SET @result = REPLACE(@result, ' LANE', ' LN')
    SET @result = REPLACE(@result, ' COURT', ' CT')
    SET @result = REPLACE(@result, ' CIRCLE', ' CIR')
    SET @result = REPLACE(@result, ' PLACE', ' PL')
    SET @result = REPLACE(@result, ' HIGHWAY', ' HWY')
    SET @result = REPLACE(@result, ' PARKWAY', ' PKWY')
    
    -- Directions
    SET @result = REPLACE(@result, ' NORTH ', ' N ')
    SET @result = REPLACE(@result, ' SOUTH ', ' S ')
    SET @result = REPLACE(@result, ' EAST ', ' E ')
    SET @result = REPLACE(@result, ' WEST ', ' W ')
    SET @result = REPLACE(@result, ' NORTHEAST ', ' NE ')
    SET @result = REPLACE(@result, ' NORTHWEST ', ' NW ')
    SET @result = REPLACE(@result, ' SOUTHEAST ', ' SE ')
    SET @result = REPLACE(@result, ' SOUTHWEST ', ' SW ')
    
    -- Unit types
    SET @result = REPLACE(@result, ' SUITE ', ' STE ')
    SET @result = REPLACE(@result, ' APARTMENT ', ' APT ')
    SET @result = REPLACE(@result, ' BUILDING ', ' BLDG ')
    SET @result = REPLACE(@result, ' FLOOR ', ' FL ')
    SET @result = REPLACE(@result, '#', ' STE ')
    
    -- Remove punctuation
    SET @result = REPLACE(@result, ',', '')
    SET @result = REPLACE(@result, '.', '')
    
    -- Normalize whitespace
    WHILE CHARINDEX('  ', @result) > 0
        SET @result = REPLACE(@result, '  ', ' ')
    
    RETURN LTRIM(RTRIM(@result))
END
GO


-- Standardize City Name
CREATE OR ALTER FUNCTION dbo.fn_StandardizeCity (
    @city NVARCHAR(100)
)
RETURNS NVARCHAR(100)
AS
BEGIN
    IF @city IS NULL RETURN ''
    
    DECLARE @result NVARCHAR(100) = UPPER(LTRIM(RTRIM(@city)))
    
    -- Common abbreviations
    SET @result = REPLACE(@result, 'SAINT ', 'ST ')
    SET @result = REPLACE(@result, 'FORT ', 'FT ')
    SET @result = REPLACE(@result, 'MOUNT ', 'MT ')
    
    -- Remove punctuation
    SET @result = REPLACE(@result, '.', '')
    SET @result = REPLACE(@result, ',', '')
    
    RETURN LTRIM(RTRIM(@result))
END
GO


-- Normalize Phone (digits only)
CREATE OR ALTER FUNCTION dbo.fn_NormalizePhone (
    @phone NVARCHAR(50)
)
RETURNS VARCHAR(20)
AS
BEGIN
    IF @phone IS NULL RETURN ''
    
    DECLARE @result VARCHAR(20) = ''
    DECLARE @i INT = 1
    DECLARE @char CHAR(1)
    
    WHILE @i <= LEN(@phone)
    BEGIN
        SET @char = SUBSTRING(@phone, @i, 1)
        IF @char LIKE '[0-9]'
            SET @result = @result + @char
        SET @i = @i + 1
    END
    
    -- Remove leading 1 if 11 digits (country code)
    IF LEN(@result) = 11 AND LEFT(@result, 1) = '1'
        SET @result = RIGHT(@result, 10)
    
    RETURN @result
END
GO


-- Normalize Postal Code
CREATE OR ALTER FUNCTION dbo.fn_NormalizePostal (
    @postal NVARCHAR(20)
)
RETURNS VARCHAR(10)
AS
BEGIN
    IF @postal IS NULL RETURN ''
    
    -- Remove non-alphanumeric
    DECLARE @result VARCHAR(10) = ''
    DECLARE @i INT = 1
    DECLARE @char CHAR(1)
    
    WHILE @i <= LEN(@postal) AND LEN(@result) < 10
    BEGIN
        SET @char = SUBSTRING(@postal, @i, 1)
        IF @char LIKE '[A-Za-z0-9]'
            SET @result = @result + UPPER(@char)
        SET @i = @i + 1
    END
    
    RETURN @result
END
GO


-- -----------------------------------------------------------------------------
-- MATCH SCORING TABLE TYPE
-- -----------------------------------------------------------------------------

CREATE TYPE dbo.MatchScoreType AS TABLE (
    company_id          INT,
    company_name        NVARCHAR(255),
    name_similarity     DECIMAL(5,2),
    postal_score        DECIMAL(5,2),
    city_score          DECIMAL(5,2),
    street_similarity   DECIMAL(5,2),
    state_match         BIT,
    phone_match         BIT,
    composite_score     DECIMAL(5,2),
    match_tier          VARCHAR(20)
)
GO


-- -----------------------------------------------------------------------------
-- MAIN MATCHING STORED PROCEDURE
-- -----------------------------------------------------------------------------

CREATE OR ALTER PROCEDURE dbo.sp_FindMatchingCompanies
    -- Input parameters (incoming company)
    @incoming_name      NVARCHAR(255),
    @incoming_street    NVARCHAR(255) = NULL,
    @incoming_city      NVARCHAR(100) = NULL,
    @incoming_state     NVARCHAR(50) = NULL,
    @incoming_postal    NVARCHAR(20) = NULL,
    @incoming_phone     NVARCHAR(50) = NULL,
    
    -- Configuration
    @high_threshold     DECIMAL(5,2) = 85.0,
    @medium_threshold   DECIMAL(5,2) = 65.0,
    @low_threshold      DECIMAL(5,2) = 50.0,
    @max_results        INT = 10,
    
    -- Weights (should sum to ~1.0)
    @name_weight        DECIMAL(3,2) = 0.45,
    @postal_weight      DECIMAL(3,2) = 0.25,
    @city_weight        DECIMAL(3,2) = 0.10,
    @street_weight      DECIMAL(3,2) = 0.15,
    @state_weight       DECIMAL(3,2) = 0.05,
    @phone_bonus        DECIMAL(5,2) = 10.0
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Standardize incoming values
    DECLARE @std_name NVARCHAR(255) = dbo.fn_StandardizeCompanyName(@incoming_name)
    DECLARE @std_street NVARCHAR(255) = dbo.fn_StandardizeStreet(@incoming_street)
    DECLARE @std_city NVARCHAR(100) = dbo.fn_StandardizeCity(@incoming_city)
    DECLARE @std_state NVARCHAR(50) = UPPER(LTRIM(RTRIM(ISNULL(@incoming_state, ''))))
    DECLARE @std_postal VARCHAR(10) = dbo.fn_NormalizePostal(@incoming_postal)
    DECLARE @std_phone VARCHAR(20) = dbo.fn_NormalizePhone(@incoming_phone)
    
    -- Results table
    DECLARE @results TABLE (
        company_id          INT,
        company_name        NVARCHAR(255),
        street_address      NVARCHAR(255),
        city                NVARCHAR(100),
        state_province      NVARCHAR(50),
        postal_code         NVARCHAR(20),
        phone               NVARCHAR(50),
        
        name_similarity     DECIMAL(5,2),
        postal_score        DECIMAL(5,2),
        city_score          DECIMAL(5,2),
        street_similarity   DECIMAL(5,2),
        state_match         BIT,
        phone_match         BIT,
        
        composite_score     DECIMAL(5,2),
        match_tier          VARCHAR(20)
    )
    
    -- Score all candidate companies
    -- First, get blocking candidates (postal match OR name SOUNDEX match)
    INSERT INTO @results (
        company_id, company_name, street_address, city, state_province, postal_code, phone,
        name_similarity, postal_score, city_score, street_similarity, state_match, phone_match,
        composite_score, match_tier
    )
    SELECT 
        c.company_id,
        c.company_name,
        a.street_address,
        a.city,
        a.state_province,
        a.postal_code,
        c.phone,
        
        -- Name similarity (using our function)
        dbo.fn_StringSimilarity(
            dbo.fn_StandardizeCompanyName(c.company_name),
            @std_name
        ) AS name_similarity,
        
        -- Postal score
        CASE 
            WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 5) = LEFT(@std_postal, 5) THEN 100.0
            WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 3) = LEFT(@std_postal, 3) THEN 60.0
            ELSE 0.0
        END AS postal_score,
        
        -- City score
        CASE 
            WHEN dbo.fn_StandardizeCity(a.city) = @std_city THEN 100.0
            WHEN dbo.fn_StringSimilarity(dbo.fn_StandardizeCity(a.city), @std_city) > 80 
                THEN dbo.fn_StringSimilarity(dbo.fn_StandardizeCity(a.city), @std_city)
            ELSE 0.0
        END AS city_score,
        
        -- Street similarity
        CASE 
            WHEN @std_street = '' OR a.street_address IS NULL THEN 0.0
            ELSE dbo.fn_StringSimilarity(
                dbo.fn_StandardizeStreet(a.street_address),
                @std_street
            )
        END AS street_similarity,
        
        -- State match
        CASE 
            WHEN @std_state != '' AND UPPER(LTRIM(RTRIM(ISNULL(a.state_province, '')))) = @std_state 
            THEN 1 ELSE 0 
        END AS state_match,
        
        -- Phone match
        CASE 
            WHEN @std_phone != '' AND LEN(@std_phone) >= 10 
                AND dbo.fn_NormalizePhone(c.phone) = @std_phone 
            THEN 1 ELSE 0 
        END AS phone_match,
        
        0.0 AS composite_score,  -- Will calculate below
        '' AS match_tier         -- Will calculate below
        
    FROM companies c
    LEFT JOIN addresses a ON a.entity_type = 'company' 
                          AND a.entity_id = c.company_id 
                          AND a.address_type = 'headquarters'
    WHERE 
        -- Blocking conditions (reduce comparison space)
        SOUNDEX(c.company_name) = SOUNDEX(@incoming_name)
        OR LEFT(dbo.fn_NormalizePostal(a.postal_code), 5) = LEFT(@std_postal, 5)
        OR (dbo.fn_StandardizeCity(a.city) = @std_city 
            AND UPPER(LTRIM(RTRIM(ISNULL(a.state_province, '')))) = @std_state)
    
    -- Calculate composite score
    UPDATE @results
    SET composite_score = 
        (name_similarity * @name_weight) +
        (postal_score * @postal_weight) +
        (city_score * @city_weight) +
        (street_similarity * @street_weight) +
        (CASE WHEN state_match = 1 THEN 100.0 ELSE 0.0 END * @state_weight) +
        (CASE WHEN phone_match = 1 THEN @phone_bonus ELSE 0.0 END)
    
    -- Cap at 100
    UPDATE @results
    SET composite_score = 100.0
    WHERE composite_score > 100.0
    
    -- Assign match tier
    UPDATE @results
    SET match_tier = CASE 
        WHEN composite_score >= @high_threshold THEN 'HIGH'
        WHEN composite_score >= @medium_threshold THEN 'MEDIUM'
        WHEN composite_score >= @low_threshold THEN 'LOW'
        ELSE 'NO_MATCH'
    END
    
    -- Return results above threshold
    SELECT TOP (@max_results)
        company_id,
        company_name,
        street_address,
        city,
        state_province,
        postal_code,
        phone,
        
        name_similarity,
        postal_score,
        city_score,
        street_similarity,
        state_match,
        phone_match,
        
        composite_score AS confidence_score,
        match_tier,
        
        -- Explanation string
        CONCAT(
            'Name: ', CAST(name_similarity AS VARCHAR), '%, ',
            'Postal: ', CAST(postal_score AS VARCHAR), '%, ',
            'City: ', CAST(city_score AS VARCHAR), '%, ',
            'Street: ', CAST(street_similarity AS VARCHAR), '%',
            CASE WHEN phone_match = 1 THEN ', Phone: MATCH' ELSE '' END
        ) AS match_explanation
        
    FROM @results
    WHERE composite_score >= @low_threshold
    ORDER BY composite_score DESC
END
GO


-- -----------------------------------------------------------------------------
-- PLANT/FACILITY MATCHING STORED PROCEDURE
-- -----------------------------------------------------------------------------

CREATE OR ALTER PROCEDURE dbo.sp_FindMatchingFacilities
    -- Input parameters
    @incoming_name      NVARCHAR(255),
    @incoming_street    NVARCHAR(255) = NULL,
    @incoming_city      NVARCHAR(100) = NULL,
    @incoming_state     NVARCHAR(50) = NULL,
    @incoming_postal    NVARCHAR(20) = NULL,
    @company_id         INT = NULL,  -- Optional: limit to specific company
    
    -- Configuration
    @threshold          DECIMAL(5,2) = 50.0,
    @max_results        INT = 10
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Standardize incoming values
    DECLARE @std_name NVARCHAR(255) = dbo.fn_StandardizeCompanyName(@incoming_name)
    DECLARE @std_street NVARCHAR(255) = dbo.fn_StandardizeStreet(@incoming_street)
    DECLARE @std_city NVARCHAR(100) = dbo.fn_StandardizeCity(@incoming_city)
    DECLARE @std_state NVARCHAR(50) = UPPER(LTRIM(RTRIM(ISNULL(@incoming_state, ''))))
    DECLARE @std_postal VARCHAR(10) = dbo.fn_NormalizePostal(@incoming_postal)
    
    SELECT TOP (@max_results)
        f.facility_id,
        f.facility_name,
        f.application_id,
        a.street_address,
        a.city,
        a.state_province,
        a.postal_code,
        
        -- Individual scores
        dbo.fn_StringSimilarity(
            dbo.fn_StandardizeCompanyName(f.facility_name),
            @std_name
        ) AS name_similarity,
        
        CASE 
            WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 5) = LEFT(@std_postal, 5) THEN 100.0
            WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 3) = LEFT(@std_postal, 3) THEN 60.0
            ELSE 0.0
        END AS postal_score,
        
        -- Composite score
        (
            dbo.fn_StringSimilarity(dbo.fn_StandardizeCompanyName(f.facility_name), @std_name) * 0.35 +
            CASE WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 5) = LEFT(@std_postal, 5) THEN 35.0
                 WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 3) = LEFT(@std_postal, 3) THEN 21.0
                 ELSE 0.0 END +
            CASE WHEN dbo.fn_StandardizeCity(a.city) = @std_city THEN 15.0 ELSE 0.0 END +
            dbo.fn_StringSimilarity(dbo.fn_StandardizeStreet(a.street_address), @std_street) * 0.15
        ) AS confidence_score,
        
        CASE 
            WHEN (
                dbo.fn_StringSimilarity(dbo.fn_StandardizeCompanyName(f.facility_name), @std_name) * 0.35 +
                CASE WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 5) = LEFT(@std_postal, 5) THEN 35.0 ELSE 0 END +
                CASE WHEN dbo.fn_StandardizeCity(a.city) = @std_city THEN 15.0 ELSE 0 END
            ) >= 85 THEN 'HIGH'
            WHEN (
                dbo.fn_StringSimilarity(dbo.fn_StandardizeCompanyName(f.facility_name), @std_name) * 0.35 +
                CASE WHEN LEFT(dbo.fn_NormalizePostal(a.postal_code), 5) = LEFT(@std_postal, 5) THEN 35.0 ELSE 0 END +
                CASE WHEN dbo.fn_StandardizeCity(a.city) = @std_city THEN 15.0 ELSE 0 END
            ) >= 65 THEN 'MEDIUM'
            ELSE 'LOW'
        END AS match_tier
        
    FROM facilities f
    LEFT JOIN addresses a ON a.entity_type = 'facility' 
                          AND a.entity_id = f.facility_id
    WHERE 
        (@company_id IS NULL OR f.application_id IN (
            SELECT application_id FROM companies WHERE company_id = @company_id
        ))
        AND (
            SOUNDEX(f.facility_name) = SOUNDEX(@incoming_name)
            OR LEFT(dbo.fn_NormalizePostal(a.postal_code), 5) = LEFT(@std_postal, 5)
            OR dbo.fn_StandardizeCity(a.city) = @std_city
        )
    ORDER BY confidence_score DESC
END
GO


-- -----------------------------------------------------------------------------
-- BATCH MATCHING FOR IMPORT PROCESSING
-- -----------------------------------------------------------------------------

CREATE OR ALTER PROCEDURE dbo.sp_BatchMatchCompanies
    @batch_id           INT,  -- ID of import batch to process
    @auto_link_high     BIT = 0,  -- Auto-link HIGH matches?
    @threshold          DECIMAL(5,2) = 50.0
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Results table for the batch
    CREATE TABLE #batch_results (
        import_row_id       INT,
        import_company_name NVARCHAR(255),
        matched_company_id  INT,
        matched_company_name NVARCHAR(255),
        confidence_score    DECIMAL(5,2),
        match_tier          VARCHAR(20),
        auto_linked         BIT DEFAULT 0
    )
    
    -- Cursor through import batch (assumes staging table structure)
    DECLARE @row_id INT, @name NVARCHAR(255), @street NVARCHAR(255)
    DECLARE @city NVARCHAR(100), @state NVARCHAR(50), @postal NVARCHAR(20)
    
    DECLARE import_cursor CURSOR FOR
        SELECT row_id, company_name, street_address, city, state, postal_code
        FROM staging_company_imports
        WHERE batch_id = @batch_id AND processed = 0
    
    OPEN import_cursor
    FETCH NEXT FROM import_cursor INTO @row_id, @name, @street, @city, @state, @postal
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Find matches for this row
        INSERT INTO #batch_results (import_row_id, import_company_name, matched_company_id, 
                                    matched_company_name, confidence_score, match_tier)
        EXEC dbo.sp_FindMatchingCompanies
            @incoming_name = @name,
            @incoming_street = @street,
            @incoming_city = @city,
            @incoming_state = @state,
            @incoming_postal = @postal,
            @low_threshold = @threshold,
            @max_results = 3
        
        FETCH NEXT FROM import_cursor INTO @row_id, @name, @street, @city, @state, @postal
    END
    
    CLOSE import_cursor
    DEALLOCATE import_cursor
    
    -- Auto-link HIGH matches if requested
    IF @auto_link_high = 1
    BEGIN
        UPDATE #batch_results
        SET auto_linked = 1
        WHERE match_tier = 'HIGH'
        AND import_row_id NOT IN (
            -- Exclude if multiple HIGH matches (ambiguous)
            SELECT import_row_id
            FROM #batch_results
            WHERE match_tier = 'HIGH'
            GROUP BY import_row_id
            HAVING COUNT(*) > 1
        )
    END
    
    -- Return results
    SELECT 
        br.*,
        CASE 
            WHEN br.match_tier = 'HIGH' AND br.auto_linked = 1 THEN 'AUTO_LINKED'
            WHEN br.match_tier = 'HIGH' THEN 'REVIEW_REQUIRED'
            WHEN br.match_tier = 'MEDIUM' THEN 'MANUAL_REVIEW'
            WHEN br.match_tier = 'LOW' THEN 'POSSIBLE_MATCH'
            ELSE 'NO_MATCH'
        END AS action_required
    FROM #batch_results br
    ORDER BY import_row_id, confidence_score DESC
    
    DROP TABLE #batch_results
END
GO


-- -----------------------------------------------------------------------------
-- AUDIT TABLE FOR MATCH DECISIONS
-- -----------------------------------------------------------------------------

CREATE TABLE match_decisions (
    decision_id         INT PRIMARY KEY IDENTITY(1,1),
    incoming_name       NVARCHAR(255) NOT NULL,
    incoming_address    NVARCHAR(500),
    matched_company_id  INT,
    confidence_score    DECIMAL(5,2),
    match_tier          VARCHAR(20),
    decision            VARCHAR(50),  -- 'LINKED', 'NEW_RECORD', 'REJECTED', 'REVIEW_PENDING'
    decided_by          NVARCHAR(100),
    decided_at          DATETIME DEFAULT GETDATE(),
    notes               NVARCHAR(MAX),
    
    FOREIGN KEY (matched_company_id) REFERENCES companies(company_id)
)
GO

CREATE INDEX idx_match_decisions_date ON match_decisions(decided_at)
CREATE INDEX idx_match_decisions_company ON match_decisions(matched_company_id)
GO


-- -----------------------------------------------------------------------------
-- EXAMPLE USAGE
-- -----------------------------------------------------------------------------

/*
-- Single company match
EXEC dbo.sp_FindMatchingCompanies
    @incoming_name = 'Acme Foods Inc.',
    @incoming_street = '123 Main Street',
    @incoming_city = 'Chicago',
    @incoming_state = 'IL',
    @incoming_postal = '60601',
    @incoming_phone = '312-555-1234'

-- Facility match
EXEC dbo.sp_FindMatchingFacilities
    @incoming_name = 'Acme Processing Plant',
    @incoming_city = 'Chicago',
    @incoming_state = 'IL',
    @incoming_postal = '60601'

-- Batch import processing
EXEC dbo.sp_BatchMatchCompanies
    @batch_id = 1,
    @auto_link_high = 1,
    @threshold = 50.0
*/
