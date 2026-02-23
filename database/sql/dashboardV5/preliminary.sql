


-- =============================================
-- 2. StageDefinitions Inserts
-- task definitions will reference these stages
-- =============================================

--INSERT INTO StageDefinitions (StageName, StageDescription, EstimatedDurationDays, CreatedBy)
--VALUES 
--('INTAKE', 'INTAKE application review', 1, 'system')


-- Stage: INTAKE (ID: 8)
-- =============================================
INSERT INTO TaskDefinitions (ProcessDefinitionId, TaskName, TaskType, TaskCategory, Sequence, StageDefinitionId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'INTAKE Stage start', 'STAGESTART', 'COMPLETION', 1, 8, 'SYSTEM', 0, 'Stage Start new application', 1, 'system'),
(1, 'ResolveCompany', 'ACTION', 'INPUT', 2, 8, 'PROD', 2880, 'Verify Company using matcher', 0, 'system'),
(1, 'ResolvePlant1', 'ACTION', 'INPUT', 3, 8, 'PROD', 2880, 'Verify Plant #1 using matcher', 0, 'system'),
(1, 'ResolvePlant2', 'ACTION', 'INPUT', 3, 8, 'PROD', 2880, 'Verify Plant #2 using matcher', 0, 'system'),
(1, 'ResolvePlant3', 'ACTION', 'INPUT', 3, 8, 'PROD', 2880, 'Verify Plant #3 using matcher', 0, 'system'),
(1, 'ResolvePlant4', 'ACTION', 'INPUT', 3, 8, 'PROD', 2880, 'Verify Plant #4 using matcher', 0, 'system'),
(1, 'ResolvePlant5', 'ACTION', 'INPUT', 3, 8, 'PROD', 2880, 'Verify Plant #5 using matcher', 0, 'system'),
--(1, 'CreateOwns', 'CONFIRM', 'CONFIRMATION', 4, 8, 'PROD', 2880, 'Create OWNS ID record', 1, 'system'),
--(1, 'GenerateWFApplication', 'CONFIRM', 'CONFIRMATION', 5, 8, 'PROD', 2880, 'Generate WFA Application', 1, 'system'),
(1, 'INTAKE Verified Gateway', 'GATEWAY', 'ESCALATION', 6, 8, 'SYSTEM', NULL, 'All Intake verifications completed', 1, 'system'),
(1, 'INTAKE App End', 'STAGEEND', 'COMPLETION', 7, 8, 'SYSTEM', 15, 'INTAKE Stage completed', 1, 'system');
GO

-- =============================================
EXEC sp_add_flow @from_name = 'INTAKE Stage start', @to_name = 'ResolveCompany', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant1', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant2', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant3', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant4', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'ResolvePlant5', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant1', @to_name = 'Prelim App End', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant2', @to_name = 'INTAKE App End', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant3', @to_name = 'INTAKE App End', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant4', @to_name = 'INTAKE App End', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant5', @to_name = 'INTAKE App End', @condition = 'None';
--EXEC sp_add_flow @from_name = 'CreateOwns', @to_name = 'GenerateWFApplication', @condition = 'None';
--EXEC sp_add_flow @from_name = 'GenerateWFApplication', @to_name = 'INTAKE Verified Gateway', @condition = 'None';
--EXEC sp_add_flow @from_name = 'INTAKE Verified Gateway', @to_name = 'INTAKE App End', @condition = 'None';
EXEC sp_add_flow @from_name = 'INTAKE App End', @to_name = 'INTAKE End', @condition = 'None';

update TaskDefinitions
set PreScriptJson = 'Company Resolver'
where TaskName = 'ResolveCompany';
GO

update TaskDefinitions
set PreScriptJson = 'Plant1 Resolver'
where TaskName = 'ResolvePlant';
GO

update TaskDefinitions
set PreScriptJson = 'Plant2 Resolver'
where TaskName = 'ResolvePlant';
GO

update TaskDefinitions
set PreScriptJson = 'Plant3 Resolver'
where TaskName = 'ResolvePlant';
GO

update TaskDefinitions
set PreScriptJson = 'Plant4 Resolver'
where TaskName = 'ResolvePlant';
GO

update TaskDefinitions
set PreScriptJson = 'Plant5 Resolver'
where TaskName = 'ResolvePlant';
GO

--UPDATE TaskDefinitions
--set PostScriptJson = 'create_wfapplication(task_instance_id, data)'
--where TaskName = 'GenerateWFApplication';
--GO