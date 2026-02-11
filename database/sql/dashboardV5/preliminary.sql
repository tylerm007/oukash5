


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
(1, 'CreateOwns', 'CONFIRM', 'CONFIRMATION', 4, 8, 'PROD', 2880, 'Create OWNS ID record', 1, 'system'),
(1, 'GenerateWFApplication', 'CONFIRM', 'CONFIRMATION', 5, 8, 'PROD', 2880, 'Generate WFA Application', 1, 'system'),
(1, 'Prelim Verified Gateway', 'GATEWAY', 'ESCALATION', 6, 8, 'SYSTEM', NULL, 'All preliminary verifications completed', 1, 'system'),
(1, 'Prelim App End', 'STAGEEND', 'COMPLETION', 7, 8, 'SYSTEM', 15, 'Preliminary Stage completed', 1, 'system');
GO

-- =============================================
EXEC sp_add_flow @from_name = 'Prelim Stage start', @to_name = 'ResolveCompany', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant', @to_name = 'CreateOwns', @condition = 'None';
EXEC sp_add_flow @from_name = 'CreateOwns', @to_name = 'GenerateWFApplication', @condition = 'None';
EXEC sp_add_flow @from_name = 'GenerateWFApplication', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'Prelim Verified Gateway', @to_name = 'Prelim App End', @condition = 'None';
--EXEC sp_add_flow @from_name = 'Prelim App End', @to_name = 'Prelim End', @condition = 'None';

update TaskDefinitions
set PreScriptJson = 'Company Resolver'
where TaskName = 'ResolveCompany';
GO

update TaskDefinitions
set PreScriptJson = 'Plant1 Resolver'
where TaskName = 'ResolvePlant';
GO

UPDATE TaskDefinitions
set PostScriptJson = 'create_wfapplication(task_instance_id, data)'
where TaskName = 'GenerateWFApplication';
GO