USE dashboard;
GO
-- Remove existing instances, definitions, and flows
DELETE FROM TaskComments;
DELETE FROM WorkflowHistory;
DELETE FROM TaskInstances;
DELETE FROM StageInstance;
DELETE FROM ProcessInstances;
DELETE FROM TaskFlow;
DELETE FROM TaskDefinitions;
GO  

-- Lane: Initial (ID: 1)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start_Application_Submitted', 'START', 'COMPLETION', 1, 1, 'SYSTEM', NULL, 'Application submitted and ready for admin review', 1, 'system'),
(1, 'Init Lane start', 'LANESTART', 'COMPLETION', 1, 1, 'SYSTEM', 0, 'Lane Start new application', 1, 'system'),
(1, 'AssignNCRC', 'ACTION', 'ASSIGNMENT', 2, 1, 'DISPATCH', 2880, 'NCRC Dispatcher Select NCRC Admin', 0, 'system'),
(1, 'verify Company', 'CONFIRM', 'CONFIRMATION', 3, 1, 'NCRC-ADMIN', 2880, 'Verify Company', 0, 'system'),
(1, 'verify Plant', 'CONFIRM', 'CONFIRMATION', 4, 1, 'NCRC-ADMIN', 2880, 'Verify Plant', 0, 'system'),
(1, 'verify Contact', 'CONFIRM', 'CONFIRMATION', 5, 1, 'NCRC-ADMIN', 2880, 'Verify Contact', 0, 'system'),
(1, 'verify Product', 'CONFIRM', 'CONFIRMATION', 6, 1, 'NCRC-ADMIN', 2880, 'Verify Product', 0, 'system'),
(1, 'verify Ingredients', 'CONFIRM', 'CONFIRMATION', 7, 1, 'NCRC-ADMIN', 2880, 'verify Ingredients', 0, 'system'),
(1, 'All Verified Gateway', 'GATEWAY', 'ESCALATION', 8, 1, 'SYSTEM', NULL, 'All verifications completed', 1, 'system'),
(1, 'to Withdrawn Y/N', 'CONDITION', 'APPROVAL', 9, 1, 'NCRC', 2880, 'Withdrawn Application Y/N', 0, 'system'),
(1, 'Assign Product', 'CONFIRM', 'ASSIGNMENT', 10, 1, 'NCRC', 2880, 'Assign to Product', 0, 'system'),
(1, 'Assign Ingredients', 'CONFIRM', 'ASSIGNMENT', 11, 1, 'NCRC', 2880, 'Assign to Ingredients', 0, 'system'),
(1, 'Contact Customer', 'CONFIRM', 'COMMUNICATION', 12, 1, 'NCRC', 2880, 'Contact Customer', 0, 'system'),
(1, 'Initial Collector', 'GATEWAY', 'ESCALATION', 13, 1, 'SYSTEM', NULL, 'Initial Collector', 1, 'system'),
(1, 'Init App End', 'LANEEND', 'COMPLETION', 14, 1, 'SYSTEM', 15, 'NDA completed', 1, 'system'),
(1, 'Lane Collector', 'GATEWAY', 'ESCALATION', 15, 1, 'SYSTEM', NULL, 'Lane Collector', 1, 'system'),
(1, 'Stage Collector', 'GATEWAY', 'ESCALATION', 17, 1, 'SYSTEM', NULL, 'Stage Collector', 1, 'system'),
(1, 'End', 'END', 'COMPLETION', 16, 1, 'SYSTEM', NULL, 'End application certification task', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'Start_Application_Submitted', @to_name = 'Init Lane Start', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Init Lane Start', @to_name = 'AssignNCRC', @condition = 'None';
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Company', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Plant', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Product', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Ingredients', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Contact', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Company', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Plant', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Contact', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Product', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'verify Ingredients', @to_name = 'All Verified Gateway', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'All Verified Gateway', @to_name = 'to Withdrawn Y/N', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'END', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Product', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Ingredients', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Contact Customer', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Assign Product', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Assign Ingredients', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Contact Customer', @to_name = 'Initial Collector', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Initial Collector', @to_name = 'Init App End', @condition = 'None';
GO
-- Lane: NDA (ID: 2)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start NDA', 'LANESTART', 'COMPLETION', 1, 2, 'NCRC', 15, 'Start NDA stage', 1, 'system'),
(1, 'Needs NDA', 'CONDITION', 'APPROVAL', 2, 2, 'NCRC', 15, 'Determine if NDA is required', 0, 'system'),
(1, 'Send NDA', 'CONFIRM', 'CONFIRMATION', 3, 2, 'LEGAL', 30, 'Send/Recieve non-disclosure agreement to customer', 0, 'system'), -- ALERT
(1, 'NDA Executed by Legal', 'CONFIRM', 'CONFIRMATION', 4, 2, 'LEGAL', 480, 'Legal review and execution of NDA', 0, 'system'),
(1, 'NDA Completed', 'CONFIRM', 'CONFIRMATION', 5, 2, 'LEGAL', 15, 'Mark NDA process as completed', 0, 'system'),
(1, 'NDA End', 'LANEEND', 'COMPLETION', 6, 2, 'SYSTEM', 15, 'NDA completed', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Start NDA', @condition = 'NO';
EXEC sp_add_flow @from_name = 'Start NDA', @to_name = 'Needs NDA', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'Send NDA', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'NDA Completed', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Send NDA', @to_name = 'NDA Executed by Legal', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'NDA Executed by Legal', @to_name = 'NDA Completed', @condition = 'NONE'; 
EXEC sp_add_flow @from_name = 'NDA Completed', @to_name = 'NDA End', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'NDA End', @to_name = 'Lane Collector', @condition = 'None';

EXEC sp_add_flow @from_name = 'NDA End', @to_name = 'Stage Collector', @condition = 'None';

GO
-- Lane: Inspection (ID: 3)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Inspection', 'LANESTART', 'COMPLETION', 1, 3, 'SYSTEM', 15, 'Start Inspection stage', 1, 'system'),
(1, 'Is Inspection Needed', 'CONDITION', 'APPROVAL', 2, 3, 'NCRC', 15, 'Is Inspection needed?', 1, 'system'),
(1, 'Assign Fee Structure', 'ACTION', 'SELECTOR', 3, 3, 'NCRC', 60, 'Calculate and set inspection fees', 0, 'system'),
(1, 'Select RFR', 'ACTION', 'ASSIGNMENT', 4, 3, 'NCRC', 30, 'Assign RFR', 0, 'system'),
(1, 'Assign Invoice Amount', 'ACTION', 'INPUT', 5, 3, 'NCRC', 30, 'Assign Kosher Inspection and Monitoring (KIM) invoice amount', 0, 'system'),
(1, 'Generated Invoice and Send', 'CONFIRM', 'CONFIRMATION', 6, 3, 'NCRC', 2880 * 3, 'Send KIM invoice to customer', 0, 'system'), -- ALERT
(1, 'Mark Invoice Paid', 'CONFIRM', 'CONFIRMATION', 7, 3, 'NCRC', 2880 * 3, 'Payment Received by Finance', 0, 'system'), -- ALERT
--(1, 'Is Payment Overdue', 'CONFIRM', 'CONFIRMATION', 8, 3, 'NCRC', 2880, 'Handle overdue payment escalation', 0, 'system'),
(1, 'Schedule Inspection', 'ACTION', 'SCHEDULING', 9, 3, 'RFR', 60, 'Schedule inspection with RFR and customer', 0, 'system'),
(1, 'Inspection Report Submitted to IAR', 'CONFIRM', 'CONFIRMATION', 11, 3, 'RFR', 240, 'Inspection report submitted to the ingredient team (IAR)', 0, 'system'),
(1, 'Withdraw Application', 'CONDITION', 'APPROVAL', 12, 3, 'NCRC', 5, 'Withdraw ApplicationY/N', 0, 'system'),
(1, 'End Inspection', 'LANEEND', 'COMPLETION', 13, 3, 'SYSTEM', 15, 'Inspection stage completed', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Start Inspection', @condition = 'NO';
EXEC sp_add_flow @from_name = 'Start Inspection', @to_name = 'Is Inspection Needed', @condition = 'None';
EXEC sp_add_flow @from_name = 'Is Inspection Needed', @to_name = 'End Inspection', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Is Inspection Needed', @to_name = 'Assign Fee Structure', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Assign Fee Structure', @to_name = 'Select RFR', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Select RFR', @to_name = 'Assign Invoice Amount', @condition = 'None';
EXEC sp_add_flow @from_name = 'Assign Invoice Amount', @to_name = 'Generated Invoice and Send', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Generated Invoice and Send', @to_name = 'Mark Invoice Paid', @condition = 'None'; 
--EXEC sp_add_flow @from_name = 'Generated Invoice and Send', @to_name = 'Is Payment Overdue', @condition = 'None';
EXEC sp_add_flow @from_name = 'Mark Invoice Paid', @to_name = 'Schedule Inspection', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Schedule Inspection', @to_name = 'Inspection Report Submitted to IAR', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Inspection Report Submitted to IAR', @to_name = 'Withdraw Application', @condition = 'None';
EXEC sp_add_flow @from_name = 'Withdraw Application', @to_name = 'End Inspection', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Withdraw Application', @to_name = 'END', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'End Inspection', @to_name = 'Lane Collector', @condition = 'None';
GO
-- Lane: Ingredients (ID: 4)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Ingredients Stage', 'LANESTART', 'COMPLETION', 1, 4, 'SYSTEM', 15, 'Start Ingredients stage', 1, 'system'),
(1, 'Upload Ingredients to KASH DB', 'CONFIRM', 'CONFIRMATION', 2, 4, 'IAR', 15, 'Upload ingredient data to KASH database', 0, 'system'),
(1, 'Verify Ingredients in DB', 'CONFIRM', 'CONFIRMATION', 3, 4, 'IAR', 15, 'Verify if all ingredient reviews are complete', 0, 'system'),
(1, 'End Ingredients', 'LANEEND', 'COMPLETION', 4, 4, 'SYSTEM', 15, 'Ingredients stage completed', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Start Ingredients Stage', @condition = 'NO';
EXEC sp_add_flow @from_name = 'Start Ingredients Stage', @to_name = 'Upload Ingredients to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload Ingredients to KASH DB', @to_name = 'Verify Ingredients in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Ingredients in DB', @to_name = 'End Ingredients', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Ingredients', @to_name = 'Lane Collector', @condition = 'None';

GO
-- Lane: Products (ID: 5)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Products Stage', 'LANESTART', 'COMPLETION', 1, 5, 'SYSTEM', 15, 'Start Products stage', 1, 'system'),
(1, 'Upload Product to KASH DB', 'CONFIRM', 'CONFIRMATION', 2, 5, 'PROD', 15, 'Upload product data to KASH database', 0, 'system'),
(1, 'Verify Products in DB', 'CONFIRM', 'CONFIRMATION', 3, 5, 'PROD', 15, 'Verify if all product reviews are complete', 0, 'system'),
(1, 'End Products', 'LANEEND', 'COMPLETION', 4, 5, 'SYSTEM', 15, 'Products stage completed', 1, 'system');

GO

EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Start Products Stage', @condition = 'NO';
EXEC sp_add_flow @from_name = 'Start Products Stage', @to_name = 'Upload Product to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload Product to KASH DB', @to_name = 'Verify Products in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Products in DB', @to_name = 'End Products', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Products', @to_name = 'Lane Collector', @condition = 'None';

GO
-- Lane: Contract (ID: 6)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Contract Stage', 'LANESTART', 'COMPLETION', 1, 6, 'LEGAL', 15, 'Start Contract stage', 1, 'system'),
(1, 'Prepare Contract', 'CONFIRM', 'CONFIRMATION', 2, 6, 'LEGAL', 240, 'Prepare contract for customer', 0, 'system'),
(1, 'Send Contract', 'CONFIRM', 'CONFIRMATION', 3, 6, 'LEGAL', 30, 'Send contract to customer for signature', 0, 'system'), -- ALERT
(1, 'Contract Signed Y/N', 'CONDITION', 'APPROVAL', 4, 6, 'LEGAL', 2880, 'Has the contract been signed?', 0, 'system'),
(1, 'End Contract', 'LANEEND', 'COMPLETION', 4, 6, 'SYSTEM', 15, 'Contract stage completed', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'Lane Collector', @to_name = 'Start Contract Stage', @condition = 'None';
EXEC sp_add_flow @from_name = 'Start Contract Stage', @to_name = 'Prepare Contract', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Prepare Contract', @to_name = 'Send Contract', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Send Contract', @to_name = 'Contract Signed Y/N', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Contract Signed Y/N', @to_name = 'End Contract', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Contract Signed Y/N', @to_name = 'END', @condition = 'NO';
EXEC sp_add_flow @from_name = 'End Contract', @to_name = 'Stage Collector', @condition = 'None';
GO

-- Lane: Certification (ID: 7)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Certification Stage', 'LANESTART', 'COMPLETION', 1, 7, 'SYSTEM', 15, 'Start Certification stage', 1, 'system'),
(1, 'Issue Certificate', 'CONFIRM', 'CONFIRMATION', 2, 7, 'RFR', 60, 'Issue certificate to customer', 0, 'system'),
(1, 'Notify Customer', 'SCRIPT', 'NOTIFICATION', 3, 7, 'RFR', 15, 'Notify customer of certification', 0, 'system'),  
(1, 'End Certification', 'LANEEND', 'COMPLETION', 4, 7, 'SYSTEM', 15, 'Certification stage completed', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'Stage Collector', @to_name = 'Start Certification Stage', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Start Certification Stage', @to_name = 'Issue Certificate', @condition = 'None';   
EXEC sp_add_flow @from_name = 'Issue Certificate', @to_name = 'Notify Customer', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Notify Customer', @to_name = 'End Certification', @condition = 'None';  
EXEC sp_add_flow @from_name = 'End Certification', @to_name = 'END', @condition = 'None'; 
GO

-- Connect Initial Lane End to other lanes
--EXEC sp_add_flow @from_name = 'Init App End', @to_name = 'Start NDA', @condition = 'None'; 
--EXEC sp_add_flow @from_name = 'Init App End', @to_name = 'Start Inspection', @condition = 'None'; 
--EXEC sp_add_flow @from_name = 'Init App End', @to_name = 'Start Ingredients Stage', @condition = 'None'; 
--EXEC sp_add_flow @from_name = 'Init App End', @to_name = 'Start Products Stage', @condition = 'None'; 

-- these two can run in parallel after collector
--EXEC sp_add_flow @from_name = 'Init App End', @to_name = 'Start Contract Stage', @condition = 'None'; 
--EXEC sp_add_flow @from_name = 'Init App End', @to_name = 'Start Certification Stage', @condition = 'None';

GO