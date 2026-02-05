


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
(1, 'ResolveCompany', 'ACTION', 'INPUT', 2, 8, 'PROD', 2880, 'Verify Company using matcher', 0, 'system'),
(1, 'ResolvePlant', 'ACTION', 'INPUT', 3, 8, 'PROD', 2880, 'Verify Plant #1 using matcher', 0, 'system'),
(1, 'Prelim Verified Gateway', 'GATEWAY', 'ESCALATION', 4, 8, 'SYSTEM', NULL, 'All preliminary verifications completed', 1, 'system'),
(1, 'Prelim App End', 'STAGEEND', 'COMPLETION', 5, 8, 'SYSTEM', 15, 'Preliminary Stage completed', 1, 'system');
GO

-- =============================================
EXEC sp_add_flow @from_name = 'Prelim Stage start', @to_name = 'ResolveCompany', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'Prelim Verified Gateway', @to_name = 'Prelim App End', @condition = 'None';
--EXEC sp_add_flow @from_name = 'Prelim App End', @to_name = 'Prelim End', @condition = 'None';

update TaskDeffinitions
set PreScriptJson = 'Company Resolver'
where TaskName = 'ResolveCompany';
GO

update TaskDeffinitions
set PreScriptJson = 'Plant1 Resolver'
where TaskName = 'ResolvePlant';
GO