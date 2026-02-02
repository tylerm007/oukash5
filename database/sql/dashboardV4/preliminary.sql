

-- =============================================
-- 1. ProcessDefinition Insert
-- =============================================
INSERT INTO ProcessDefinitions (ProcessName, ProcessVersion, Description, IsActive, CreatedBy)
VALUES ('Preliminary Application', '1.0', 'OU Kosher preliminary application process', 1, 'SYSTEM');
GO
-- =============================================
-- 2. StageDefinitions Inserts
-- task definitions will reference these stages
-- =============================================

INSERT INTO StageDefinitions (StageName, StageDescription, EstimatedDurationDays, CreatedBy)
VALUES 
('Preliminary', 'Preliminary application review', 1, 'system')


-- Stage: Preliminary (ID: 2)
INSERT INTO TaskDefinitions (ProcessDefinitionId, TaskName, TaskType, TaskCategory, Sequence, StageDefinitionId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(2, 'Application_Submitted', 'START', 'COMPLETION', 1, 2, 'SYSTEM', NULL, 'JotForm Application submitted', 1, 'system'),
(2, 'Prelim Stage start', 'STAGESTART', 'COMPLETION', 1, 2, 'SYSTEM', 0, 'Stage Start new application', 1, 'system'),
(2, 'ResolveCompany', 'ACTION', 'ASSIGNMENT', 2, 2, 'DISPATCH', 2880, 'Verify Company using matcher', 0, 'system'),
(2, 'ResolvePlant', 'ACTION', 'ASSIGNMENT', 2, 2, 'DISPATCH', 2880, 'Verify Plant using matcher', 0, 'system'),
(2, 'Withdrawn App', 'CONDITION', 'APPROVAL', 3, 2, 'NCRC', 2880, 'Withdrawn Application Y/N', 0, 'system'),
(2, 'Prelim Verified Gateway', 'GATEWAY', 'ESCALATION', 4, 2, 'SYSTEM', NULL, 'All verifications completed', 1, 'system'),
(2, 'Prelim App End', 'STAGEEND', 'COMPLETION', 5, 2, 'SYSTEM', 15, 'NDA completed', 1, 'system'),
(2, 'Prelim Stage Collector', 'GATEWAY', 'ESCALATION', 6, 2, 'SYSTEM', NULL, 'Stage Collector', 1, 'system'),
(2, 'App End', 'END', 'COMPLETION', 7, 2, 'SYSTEM', NULL, 'End application certification task', 1, 'system');
GO

-- =============================================
EXEC sp_add_flow @from_name = 'Application_Submitted', @to_name = ''Prelim Stage start', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Prelim Stage start', @to_name = 'ResolveCompany', @condition = 'None';
EXEC sp_add_flow @from_name = 'Prelim Stage start', @to_name = 'ResolvePlant', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolveCompany', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'ResolvePlant', @to_name = 'Prelim Verified Gateway', @condition = 'None';
EXEC sp_add_flow @from_name = 'Withdrawn App', @to_name = 'Prelim Verified Gateway', @condition = 'No';
EXEC sp_add_flow @from_name = 'Withdrawn App', @to_name = 'Prelim Stage Collector', @condition = 'Yes';
EXEC sp_add_flow @from_name = 'Prelim Verified Gateway', @to_name = 'Withdrawn App', @condition = 'None';
EXEC sp_add_flow @from_name = 'Prelim Stage Collector', @to_name = 'App End', @condition = 'None';