


-- =============================================
-- 2. StageDefinitions Inserts
-- task definitions will reference these stages
-- =============================================

--INSERT INTO StageDefinitions (StageName, StageDescription, EstimatedDurationDays, CreatedBy)
--VALUES 
--('Preliminary', 'Preliminary application review', 1, 'system')


-- Stage: Preliminary (ID: 8)
-- =============================================
INSERT INTO TaskDefinitions (ProcessDefinitionId, TaskName, TaskType, TaskCategory, Sequence, StageDefinitionId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Prelim Stage start', 'STAGESTART', 'COMPLETION', 1, 8, 'SYSTEM', 0, 'Stage Start new application', 1, 'system'),
(1, 'Withdrawn App', 'CONDITION', 'APPROVAL', 3, 8, 'ADMIN', 2880, 'Withdrawn Application Submission Y/N', 0, 'system'),
(1, 'ResolveCompany', 'ACTION', 'RESOLVER', 2, 8, 'ADMIN', 2880, 'Verify Company using matcher', 0, 'system'),
(1, 'ResolvePlant1', 'ACTION', 'RESOLVER', 2, 8, 'ADMIN', 2880, 'Verify Plant #1 using matcher', 0, 'system'),
(1, 'ResolvePlant2', 'ACTION', 'RESOLVER', 2, 8, 'ADMIN', 2880, 'Verify Plant #2 using matcher', 0, 'system'),
(1, 'ResolvePlant3', 'ACTION', 'RESOLVER', 2, 8, 'ADMIN', 2880, 'Verify Plant #3 using matcher', 0, 'system'),
(1, 'ResolvePlant4', 'ACTION', 'RESOLVER', 2, 8, 'ADMIN', 2880, 'Verify Plant #4 using matcher', 0, 'system'),
(1, 'ResolvePlant5', 'ACTION', 'RESOLVER', 2, 8, 'ADMIN', 2880, 'Verify Plant #5 using matcher', 0, 'system'),
(1, 'Prelim Verified Gateway', 'GATEWAY', 'ESCALATION', 4, 8, 'SYSTEM', NULL, 'All preliminary verifications completed', 1, 'system'),
(1, 'Prelim App End', 'STAGEEND', 'COMPLETION', 5, 8, 'SYSTEM', 15, 'Preliminary Stage completed', 1, 'system');
GO

-- =============================================
EXEC sp_add_flow @from_name = 'Prelim Stage start', @to_name = 'Withdrawn App', @condition = 'None';
EXEC sp_add_flow @from_name = 'Withdrawn App', @to_name = 'ResolveCompany', @condition = 'No';
EXEC sp_add_flow @from_name = 'Withdrawn App', @to_name = 'Prelim App End', @condition = 'Yes';

EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant1', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant2', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant3', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant4', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant5', @condition = 'None';

EXEC sp_add_flow @from_name = 'ResolvePlant1', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant2', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant3', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant4', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant5', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'Prelim Verified Gateway', @to_name = 'Prelim App End', @condition = 'None';
--EXEC sp_add_flow @from_name = 'Prelim App End', @to_name = 'Prelim End', @condition = 'None';