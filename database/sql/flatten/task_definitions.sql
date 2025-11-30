USE dashboardV1;
GO
-- Remove existing instances, definitions, and flows
IF OBJECT_ID('dbo.TaskComments', 'U') IS NOT NULL DELETE FROM TaskComments;
IF OBJECT_ID('dbo.WorkflowHistory', 'U') IS NOT NULL DELETE FROM WorkflowHistory;
IF OBJECT_ID('dbo.TaskInstances', 'U') IS NOT NULL DELETE FROM TaskInstances;
IF OBJECT_ID('dbo.StageInstance', 'U') IS NOT NULL DELETE FROM StageInstance;
IF OBJECT_ID('dbo.ProcessInstances', 'U') IS NOT NULL DELETE FROM ProcessInstances;
IF OBJECT_ID('dbo.TaskFlow', 'U') IS NOT NULL DELETE FROM TaskFlow;
IF OBJECT_ID('dbo.TaskDefinitions', 'U') IS NOT NULL DELETE FROM TaskDefinitions;
GO  

IF OBJECT_ID('dbo.TaskComments', 'U') IS NOT NULL DROP TABLE TaskComments;
IF OBJECT_ID('dbo.WorkflowHistory', 'U') IS NOT NULL DROP TABLE WorkflowHistory;
IF OBJECT_ID('dbo.TaskInstances', 'U') IS NOT NULL DROP TABLE TaskInstances;
IF OBJECT_ID('dbo.StageInstance', 'U') IS NOT NULL DROP TABLE StageInstance;
IF OBJECT_ID('dbo.ProcessInstances', 'U') IS NOT NULL DROP TABLE ProcessInstances;
IF OBJECT_ID('dbo.TaskFlow', 'U') IS NOT NULL DROP TABLE TaskFlow;
IF OBJECT_ID('dbo.TaskDefinitions', 'U') IS NOT NULL DROP TABLE TaskDefinitions;
GO  



-- =============================================
-- STORED PROCEDURE to Add TaskFlow
-- =============================================

-- Stored Procedure: sp_add_flow
-- Purpose: Add a new task flow by looking up TaskDefinition IDs by TaskName
-- Parameters: 
--   @from_name - TaskName of the source task (can be NULL for start flows)
--   @to_name - TaskName of the destination task
--   @condition - Flow condition (optional)
-- =============================================

CREATE OR ALTER PROCEDURE sp_add_flow
    @from_name NVARCHAR(100) = NULL,
    @to_name NVARCHAR(100),
    @condition NVARCHAR(500) = NULL
AS
BEGIN
   
    
    DECLARE @from_task_id INT = NULL;
    DECLARE @to_task_id INT;
    DECLARE @error_msg NVARCHAR(500);
    SET NOCOUNT ON;
    
    BEGIN TRY
        -- Look up the ToTask ID (required)
        SELECT @to_task_id = TaskId 
        FROM TaskDefinitions 
        WHERE TaskName = @to_name;
        
        IF @to_task_id IS NULL
        BEGIN
            SET @error_msg = 'ToTask not found: ' + @to_name;
            THROW 50001, @error_msg, 1;
        END
        
        -- Look up the FromTask ID (optional for start flows)
        IF @from_name IS NOT NULL
        BEGIN
            SELECT @from_task_id = TaskId 
            FROM TaskDefinitions 
            WHERE TaskName = @from_name;
            
            IF @from_task_id IS NULL
            BEGIN
                SET @error_msg = 'FromTask not found: ' + @from_name;
                THROW 50002, @error_msg, 1;
            END
        END
        
        -- Check if flow already exists
        IF EXISTS (
            SELECT 1 FROM TaskFlow 
            WHERE FromTaskId = @from_task_id 
            AND ToTaskId = @to_task_id
            AND ISNULL(Condition, '') = ISNULL(@condition, '')
        )
        BEGIN
            SET @error_msg = 'Flow already exists from ''' + ISNULL(@from_name, 'START') + ''' to ''' + @to_name + '''';
            THROW 50003, @error_msg, 1;
        END
        
        -- Insert the new flow
        INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
        VALUES (@from_task_id, @to_task_id, @condition, 0);
        
        -- Return success message
        SELECT 
            SCOPE_IDENTITY() as FlowId,
            @from_task_id as FromTaskId,
            @to_task_id as ToTaskId,
            @from_name as FromTaskName,
            @to_name as ToTaskName,
            @condition as Condition,
            'Flow added successfully' as Message;
            
    END TRY
    BEGIN CATCH
        -- Return error information
        SELECT 
            ERROR_NUMBER() as ErrorNumber,
            ERROR_MESSAGE() as ErrorMessage,
            ERROR_SEVERITY() as ErrorSeverity,
            ERROR_STATE() as ErrorState;
    END CATCH
END;
GO

-- Lane: Initial (ID: 1)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start_Application_Submitted', 'START', 'COMPLETION', 1, 1, 'SYSTEM', NULL, 'Application submitted and ready for admin review', 1, 'system'),
(1, 'Init Lane start', 'LANESTART', 'COMPLETION', 1, 1, 'SYSTEM', 0, 'Lane Start new application', 1, 'system'),
(1, 'AssignNCRC', 'ACTION', 'ASSIGNMENT', 2, 1, 'DISPATCH', 2880, 'NCRC Dispatcher Select NCRC Admin', 0, 'system'),
(1, 'All Verified Gateway', 'GATEWAY', 'ESCALATION', 8, 1, 'SYSTEM', NULL, 'All verifications completed', 1, 'system'),
(1, 'to Withdrawn Y/N', 'CONDITION', 'APPROVAL', 9, 1, 'NCRC', 2880, 'Withdrawn Application Y/N', 0, 'system'),
(1, 'Assign Product', 'CONFIRM', 'CONFIRMATION', 10, 1, 'NCRC', 2880, 'Assign to Product', 0, 'system'),
(1, 'Assign Ingredients', 'CONFIRM', 'CONFIRMATION', 11, 1, 'NCRC', 2880, 'Assign to Ingredients', 0, 'system'),
(1, 'Contact Customer', 'CONFIRM', 'CONFIRMATION', 12, 1, 'NCRC', 2880, 'Contact Customer', 0, 'system'),
(1, 'Initial Collector', 'GATEWAY', 'ESCALATION', 13, 1, 'SYSTEM', NULL, 'Initial Collector', 1, 'system'),
(1, 'Init App End', 'LANEEND', 'COMPLETION', 14, 1, 'SYSTEM', 15, 'NDA completed', 1, 'system'),
(1, 'Stage Collector', 'GATEWAY', 'ESCALATION', 15, 1, 'SYSTEM', NULL, 'Stage Collector', 1, 'system'),
(1, 'End', 'END', 'COMPLETION', 17, 1, 'SYSTEM', NULL, 'End application certification task', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'Start_Application_Submitted', @to_name = 'Init Lane Start', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Init Lane Start', @to_name = 'AssignNCRC', @condition = 'None';
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'All Verified Gateway', @condition = 'None'; 
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
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'NDA End', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Send NDA', @to_name = 'NDA Executed by Legal', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'NDA Executed by Legal', @to_name = 'NDA Completed', @condition = 'NONE'; 
EXEC sp_add_flow @from_name = 'NDA Completed', @to_name = 'NDA End', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'NDA End', @to_name = 'Stage Collector', @condition = 'None';

GO
-- Lane: Inspection (ID: 3)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Inspection', 'LANESTART', 'COMPLETION', 1, 3, 'SYSTEM', 15, 'Start Inspection stage', 1, 'system'),
(1, 'Is Inspection Needed', 'CONDITION', 'APPROVAL', 2, 3, 'NCRC', 15, 'Is Inspection needed?', 0, 'system'),
(1, 'Assign Fee Structure', 'ACTION', 'SELECTOR', 3, 3, 'NCRC', 60, 'Calculate and set inspection fees', 0, 'system'),
(1, 'Select RFR', 'ACTION', 'ASSIGNMENT', 4, 3, 'NCRC', 30, 'Assign RFR', 0, 'system'),
(1, 'Assign Invoice Amount', 'ACTION', 'INPUT', 5, 3, 'NCRC', 30, 'Assign Kosher Inspection and Monitoring (KIM) invoice amount', 0, 'system'),
(1, 'Generated Invoice and Send', 'CONFIRM', 'CONFIRMATION', 6, 3, 'NCRC', 2880 * 3, 'Send KIM invoice to customer', 0, 'system'), -- ALERT
(1, 'Mark Invoice Paid', 'CONFIRM', 'CONFIRMATION', 7, 3, 'NCRC', 2880 * 3, 'Payment Received by Finance', 0, 'system'), -- ALERT
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
EXEC sp_add_flow @from_name = 'Mark Invoice Paid', @to_name = 'Schedule Inspection', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Schedule Inspection', @to_name = 'Inspection Report Submitted to IAR', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Inspection Report Submitted to IAR', @to_name = 'Withdraw Application', @condition = 'None';
EXEC sp_add_flow @from_name = 'Withdraw Application', @to_name = 'End Inspection', @condition = 'NO'; 
EXEC sp_add_flow @from_name = 'Withdraw Application', @to_name = 'END', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'End Inspection', @to_name = 'Stage Collector', @condition = 'None';
GO
-- Lane: Ingredients (ID: 4)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Ingredients Stage', 'LANESTART', 'COMPLETION', 1, 4, 'SYSTEM', 15, 'Start Ingredients stage', 1, 'system'),
(1, 'Upload Ingredients to KASH DB', 'CONFIRM', 'CONFIRMATION', 2, 4, 'IAR', 15, 'Upload ingredient data to KASH database', 0, 'system'),
(1, 'Verify Ingredients in DB', 'CONFIRM', 'CONFIRMATION', 3, 4, 'IAR', 15, 'Verify if all ingredient reviews are complete', 0, 'system'),
(1, 'End Ingredients', 'LANEEND', 'COMPLETION', 4, 4, 'SYSTEM', 15, 'Ingredients stage completed', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'Assign Ingredients', @to_name = 'Start Ingredients Stage', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Start Ingredients Stage', @to_name = 'Upload Ingredients to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload Ingredients to KASH DB', @to_name = 'Verify Ingredients in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Ingredients in DB', @to_name = 'End Ingredients', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Ingredients', @to_name = 'Stage Collector', @condition = 'None';

GO
-- Lane: Products (ID: 5)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Products Stage', 'LANESTART', 'COMPLETION', 1, 5, 'SYSTEM', 15, 'Start Products stage', 1, 'system'),
(1, 'Upload Product to KASH DB', 'CONFIRM', 'CONFIRMATION', 2, 5, 'PROD', 15, 'Upload product data to KASH database', 0, 'system'),
(1, 'Verify Products in DB', 'CONFIRM', 'CONFIRMATION', 3, 5, 'PROD', 15, 'Verify if all product reviews are complete', 0, 'system'),
(1, 'End Products', 'LANEEND', 'COMPLETION', 4, 5, 'SYSTEM', 15, 'Products stage completed', 1, 'system');

GO
EXEC sp_add_flow @from_name = 'Assign Product', @to_name = 'Start Products Stage', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Start Products Stage', @to_name = 'Upload Product to KASH DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Upload Product to KASH DB', @to_name = 'Verify Products in DB', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Verify Products in DB', @to_name = 'End Products', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'End Products', @to_name = 'Stage Collector', @condition = 'None';

GO
-- Lane: Contract (ID: 6)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Contract Stage', 'LANESTART', 'COMPLETION', 1, 6, 'SYSTEM', 15, 'Start Contract stage', 1, 'system'),
(1, 'Prepare Contract', 'CONFIRM', 'CONFIRMATION', 2, 6, 'LEGAL', 240, 'Prepare contract for customer', 0, 'system'),
(1, 'Send Contract', 'CONFIRM', 'CONFIRMATION', 3, 6, 'LEGAL', 30, 'Send contract to customer for signature', 0, 'system'), -- ALERT
(1, 'Contract Signed Y/N', 'CONDITION', 'APPROVAL', 4, 6, 'LEGAL', 2880, 'Has the contract been signed?', 0, 'system'),
(1, 'End Contract', 'LANEEND', 'COMPLETION', 4, 6, 'SYSTEM', 15, 'Contract stage completed', 1, 'system');
GO

EXEC sp_add_flow @from_name = 'Stage Collector', @to_name = 'Start Contract Stage', @condition = 'None';
EXEC sp_add_flow @from_name = 'Start Contract Stage', @to_name = 'Prepare Contract', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Prepare Contract', @to_name = 'Send Contract', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Send Contract', @to_name = 'Contract Signed Y/N', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Contract Signed Y/N', @to_name = 'End Contract', @condition = 'YES'; 
EXEC sp_add_flow @from_name = 'Contract Signed Y/N', @to_name = 'END', @condition = 'NO';
---EXEC sp_add_flow @from_name = 'End Contract', @to_name = 'Stage Collector', @condition = 'None';
GO

-- Lane: Certification (ID: 7)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
(1, 'Start Certification Stage', 'LANESTART', 'COMPLETION', 1, 7, 'SYSTEM', 15, 'Start Certification stage', 1, 'system'),
(1, 'Issue Certificate', 'CONFIRM', 'CONFIRMATION', 2, 7, 'NCRC', 60, 'Issue certificate to customer', 0, 'system'),
(1, 'Notify Customer', 'CONFIRM', 'CONFIRMATION', 3, 7, 'NCRC', 15, 'Notify customer of certification', 0, 'system'),  
(1, 'End Certification', 'LANEEND', 'COMPLETION', 4, 7, 'SYSTEM', 15, 'Certification stage completed', 1, 'system');
GO
EXEC sp_add_flow @from_name = 'End Contract', @to_name = 'Start Certification Stage', @condition = 'None';
EXEC sp_add_flow @from_name = 'Start Certification Stage', @to_name = 'Issue Certificate', @condition = 'None';   
EXEC sp_add_flow @from_name = 'Issue Certificate', @to_name = 'Notify Customer', @condition = 'None'; 
EXEC sp_add_flow @from_name = 'Notify Customer', @to_name = 'End Certification', @condition = 'None';  
EXEC sp_add_flow @from_name = 'End Certification', @to_name = 'END', @condition = 'None'; 
GO


-- IN PROGRESS
UPDATE TaskDefinitions
set PostScriptJson = 'set_application_attribute(application_id,"Status","INP", data)'
where TaskType = 'START';
GO

UPDATE TaskDefinitions
set PostScriptJson = 'set_application_attribute(application_id,"Status","INSPECTION", data)'
where TaskName = 'Schedule Inspection';
GO

UPDATE TaskDefinitions
set PostScriptJson = 'set_application_attribute(application_id,"Status","REVIEW", data)'
where TaskName = 'Inspection Report Submitted to IAR';
GO


UPDATE TaskDefinitions
set PostScriptJson = 'set_application_attribute(application_id,"Status","CONTRACT", data)'
where TaskName = 'Send Contract';
GO

UPDATE TaskDefinitions
set PostScriptJson = 'set_stage_attribute(stage_id,"Status","IN_PROGRESS", data)'
where TaskType = 'LANESTART';

UPDATE TaskDefinitions
set PostScriptJson = 'set_stage_attribute(stage_id,"Status","COMPLETED", data)'
where TaskType = 'LANEEND';
GO

UPDATE TaskDefinitions
set PostScriptJson = '''
if task.Result == "YES":
    set_application_attribute(application_id,"Status","WTH", data)
'''
where TaskName = 'to Withdrawn Y/N';
GO

UPDATE TaskDefinitions
set PostScriptJson = 'set_application_attribute(application_id,"Status","COMPL", data)'
where TaskName = 'Issue Certificate';
GO

UPDATE TaskDefinitions
set PostScriptJson = '''
if task.Result == "YES":
    set_application_attribute(application_id,"Status","WTH", data)
'''
where TaskName = 'Withdraw Application';
GO


UPDATE TaskDefinitions
set   PostScriptJson = 'create_invoice(task_instance_id,  data)'
where TaskName = 'Generated Invoice and Send';
GO