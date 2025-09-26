use dashboard;

-- =============================================
-- Additional Reference Data Inserts
-- =============================================

-- Lane Roles (if not already exist)
INSERT INTO LaneRoles (RoleCode, RoleDescription) VALUES
('NCRC', 'NCRC Coordinator'),
('NCRCADMIN', 'NCRC Administrator'),
('DISPATCH', 'Dispatcher Role'),
('ADMIN', 'System Administrator'),
('LEGAL', 'Legal Department'),
('INSP', 'Inspection Team'),
('IAR', 'Ingredients Review Team'),
('PROD', 'Products Department'),
('RC', 'Rabbinical Coordinator'),
('CERT', 'Certification Team'),
('BILLING', 'Billing Department'),
('IAR_MANAGER', 'IAR Manager'),
('PROD_MANAGER', 'Products Manager'),
('RC_MANAGER', 'RC Manager'),
('RFR', 'Rabbinical Field Representative'),
('SYSTEM', 'System Automated');


-- Task Types
INSERT INTO TaskTypes (TaskTypeCode, TaskTypeDescription) VALUES
('CONFIRM', 'User Confirmation Task - Requires human interaction'),
('ACTION', 'User Action Task - Requires human interaction'),
('USER', 'User Task - Requires human interaction'),
('SYSTEM', 'System Task - Automated execution'),
('START', 'Process Start Event'),
('END', 'Process End Event'),
('SERVICE', 'Service Task - External service call'),
('SCRIPT', 'Script Task - Executes a script'),
('CONDITION', 'Condition Task - Evaluates a condition'),
('GATEWAY', 'Gateway - Decision point');

-- Task Categories
INSERT INTO TaskCategories (TaskCategoryCode, TaskCategoryDescription) VALUES
('REVIEW', 'Review and Analysis Tasks'),
('ASSIGNMENT', 'Task Assignment Activities'),
('COMMUNICATION', 'Communication and Correspondence'),
('APPROVAL', 'Approval and Authorization'),
('COMPLETION', 'Task Completion Activities'),
('FINANCIAL', 'Financial and Billing Tasks'),
('ESCALATION', 'Escalation and Exception Handling'),
('NOTIFICATION', 'System Notifications'),
('CONFIRMATION', 'User Confirmation'),
('SCHEDULING', 'Scheduling and Planning'),
('VERIFICATION', 'Data and Status Verification');
 
 
-- Process Status
INSERT INTO ProcessStatus (StatusCode, StatusDescription) VALUES
('NEW', 'New Process Instance'),
('RUNNING', 'Process Currently Running'),
('COMPLETED', 'Process Completed Successfully'),
('FAILED', 'Process Failed'),
('SUSPENDED', 'Process Suspended'),
('TERMINATED', 'Process Terminated');


-- Process Priorities
INSERT INTO ProcessPriorities (PriorityCode, PriorityDescription) VALUES
('LOW', 'Low Priority'),
('NORMAL', 'Normal Priority'),
('HIGH', 'High Priority'),
('URGENT', 'Urgent Priority');

-- Stage Status
INSERT INTO StageStatus (StatusCode, StatusDescription) VALUES
('NEW', 'New Stage'),
('IN_PROGRESS', 'Stage In Progress'),
('COMPLETED', 'Stage Completed'),
('ON_HOLD', 'Stage On Hold'),
('CANCELLED', 'Stage Cancelled');

-- Task Status
INSERT INTO TaskStatus (StatusCode, StatusDescription) VALUES
('PENDING', 'Task Pending Execution'),
('RUNNING', 'Task Currently Running'),
('COMPLETED', 'Task Completed Successfully'),
('FAILED', 'Task Failed'),
('SKIPPED', 'Task Skipped'),
('CANCELLED', 'Task Cancelled');

-- Process Message Types
INSERT INTO ProcessMessageTypes (MessageTypeCode, MessageTypeDescription) VALUES
    ('STANDARD', 'Standard message'),
    ('URGENT', 'Urgent message requiring immediate attention'),
    ('SYSTEM', 'System-generated message'),
    ('NOTIFICATION', 'Notification message');

-- Task Comment Types
INSERT INTO TaskCommentTypes (CommentTypeCode, CommentTypeDescription) VALUES
    ('INTERNAL', 'Internal comment for staff use only'),
    ('EXTERNAL', 'External comment visible to clients'),
    ('SYSTEM', 'System-generated comment');

GO
-- =============================================
-- Insert Process Definition and Tasks
-- =============================================

-- =============================================
-- 1. ProcessDefinition Insert
-- =============================================


-- =============================================
-- 1. ProcessDefinition Insert
-- =============================================
INSERT INTO ProcessDefinitions (ProcessName, ProcessVersion, Description, IsActive, CreatedBy)
VALUES ('OU Application Init', '1.0', 'OU Kosher initial application process', 1, 'SYSTEM');
GO
-- =============================================
-- 2. LaneDefinition Inserts
-- =============================================
INSERT INTO LaneDefinitions (ProcessId, LaneName, LaneDescription, EstimatedDurationDays, LaneRole, CreatedBy)
VALUES 
(1, 'Initial', 'Initial application review and task assignment', 2, 'NCRC', 'system'),
(1, 'NDA', 'Non-disclosure agreement handling and execution', 3, 'LEGAL', 'system'),
(1, 'Inspection', 'Plant inspection and RFR assignment process', 10, 'RC', 'system'),
(1, 'Ingredients', 'IAR ingredients and kosher code review process', 7, 'IAR', 'system'),
(1, 'Products', 'Product evaluation and PLA processing', 5, 'PROD', 'system'),
(1, 'Contract', 'Contract review and certification agreement', 3, 'LEGAL', 'system'),
(1, 'Certification', 'Final certification and invoice processing', 2, 'CERT', 'system');
GO
-- Insert Task Definitions for initial application Workflow
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete, CreatedBy)
VALUES
    (1, 'Start_Application_Submitted', 'START', 'COMPLETION', 1, 1, 'SYSTEM', NULL, 'Application submitted and ready for admin review', 1,'system'),
    (1, 'AssignNCRC', 'ACTION', 'ASSIGNMENT', 2, 1, 'DISPATCH', 2880, 'NCRC Dispatcher Select NCRC Admin', 0,'system'),
    (1, 'verify Company', 'CONFIRM', 'CONFIRMATION', 3, 1, 'NCRC-ADMIN', 2880, 'Verify Company', 0,'system'),
    (1, 'verify Plant', 'CONFIRM', 'CONFIRMATION', 4, 1, 'NCRC-ADMIN', 2880, 'Verify Plant', 0,'system'),
    (1, 'verify Contact', 'CONFIRM', 'CONFIRMATION', 5, 1, 'NCRC-ADMIN', 2880, 'Verify Contact', 0,'system'),
    (1, 'verify Product', 'CONFIRM', 'CONFIRMATION', 6, 1, 'NCRC-ADMIN', 2880, 'Verify Product', 0,'system'),
    (1, 'verify Ingredients', 'CONFIRM', 'CONFIRMATION', 7, 1, 'NCRC-ADMIN', 2880, 'verify Ingredients', 0,'system'),
    (1, 'All Verified Gateway', 'GATEWAY', 'ESCALATION', 8, 1, 'SYSTEM', NULL, 'All verifications completed', 1,'system'),
    (1, 'to Withdrawn Y/N', 'CONDITION', 'APPROVAL', 9, 1, 'NCRC', 2880, 'Withdrawn Application Y/N', 0,'system'),
    (1, 'Assign Product', 'CONFIRM', 'ASSIGNMENT', 10, 1, 'NCRC', 2880, 'Assign to Product', 0,'system'),
    (1, 'Assign Ingredients', 'CONFIRM', 'ASSIGNMENT', 11, 1, 'NCRC', 2880, 'Assign to Ingredients', 0,'system'),
    (1, 'Contact Customer', 'CONFIRM', 'COMMUNICATION', 12, 1, 'NCRC', 2880, 'Contact Customer', 0,'system'),
    (1, 'Initial Collector', 'GATEWAY', 'ESCALATION', 13, 1, 'SYSTEM', NULL, 'Initial Collector', 1,'system'),
    (1, 'End', 'END', 'COMPLETION', 14, 1, 'SYSTEM', NULL, 'end task', 1,'system');

GO

-- task flow for tasks in lane 1
--INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
EXEC sp_add_flow @from_name = 'Start_Application_Submitted', @to_name = 'AssignNCRC', @condition = NULL;
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Company', @condition = NULL;
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Plant', @condition = NULL;
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Contact', @condition = NULL;
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Product', @condition = NULL;
EXEC sp_add_flow @from_name = 'AssignNCRC', @to_name = 'verify Ingredients', @condition = NULL;
EXEC sp_add_flow @from_name = 'verify Company', @to_name = 'All Verified Gateway', @condition = NULL;
EXEC sp_add_flow @from_name = 'verify Plant', @to_name = 'All Verified Gateway', @condition = NULL;
EXEC sp_add_flow @from_name = 'verify Contact', @to_name = 'All Verified Gateway', @condition = NULL;
EXEC sp_add_flow @from_name = 'verify Product', @to_name = 'All Verified Gateway', @condition = NULL;
EXEC sp_add_flow @from_name = 'verify Ingredients', @to_name = 'All Verified Gateway', @condition = NULL;
EXEC sp_add_flow @from_name = 'All Verified Gateway', @to_name = 'to Withdrawn Y/N', @condition = NULL;
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'End', @condition = 'YES';
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Product', @condition = 'NO';
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Assign Ingredients', @condition = 'NO';
EXEC sp_add_flow @from_name = 'to Withdrawn Y/N', @to_name = 'Contact Customer', @condition = 'NO';
EXEC sp_add_flow @from_name = 'Assign Product', @to_name = 'Initial Collector', @condition = NULL;
EXEC sp_add_flow @from_name = 'Assign Ingredients', @to_name = 'Initial Collector', @condition = NULL;
EXEC sp_add_flow @from_name = 'Contact Customer', @to_name = 'Initial Collector', @condition = NULL;
EXEC sp_add_flow @from_name = 'Initial Collector', @to_name = 'End', @condition = NULL;
GO
-- ============================================= STOP HERE FOR TESTING =======================

INSERT INTO ProcessDefinitions (ProcessName, ProcessVersion, Description, IsActive, CreatedBy)
VALUES ('OU Certification Workflow', '1.0', 'Complete workflow for OU Kosher certification process', 1, 'system');


-- =============================================
-- 3. TaskDefinition Inserts
-- =============================================
-- Initial Processing Lane Tasks (LaneId = 1)
--INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description, CreatedBy)
--VALUES
--(1, 'Evaluate Application', 'CONFIRM', 'CONFIRMATION', 1, 1, 0, 'NCRC', 120, 1, 0, 'Initial evaluation of certification application', 'system'),
--(1, 'Assign to Products', 'ACTION', 'ASSIGNMENT', 2, 1, 1, 'NCRC', 15, 1, 0, 'Assign application to Products Department', 'system'),
--(1, 'Assign to IAR', 'ACTION', 'ASSIGNMENT', 3, 1, 1, 'NCRC', 15, 1, 0, 'Assign application to Ingredients Review', 'system'),
--(1, 'Contact Customer', 'CONFIRM', 'CONFIRMATION', 4, 1, 1, 'NCRC', 30, 1, 0, 'Initial customer contact for information gathering', 'system');
--EXEC sp_add_flow @from_name = 'Evaluate Application', @to_name = 'Assign to Products', @condition = NULL;
--EXEC sp_add_flow @from_name = 'Evaluate Application', @to_name = 'Assign to IAR', @condition = NULL;
--EXEC sp_add_flow @from_name = 'Evaluate Application', @to_name = 'Contact Customer', @condition = NULL;
--EXEC sp_add_flow @from_name = 'Assign to Products', @to_name = 'End', @condition = NULL;
--EXEC sp_add_flow @from_name = 'Assign to IAR', @to_name = 'End', @condition = NULL;
--EXEC sp_add_flow @from_name = 'Contact Customer', @to_name = 'End', @condition = NULL;

-- NDA Processing Lane Tasks (LaneId = 2)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description, CreatedBy)
VALUES
(1, 'Start NDA', 'START', 'COMPLETION', 4, 2, 0, 'NCRC', 15, 0, 1, 'Start NDA stage', 'system'),
(1, 'Needs NDA', 'CONDITION', 'APPROVAL', 4, 2, 0, 'NCRC', 15, 0, 0, 'Determine if NDA is required', 'system'),
(1, 'Send NDA', 'CONFIRM', 'CONFIRMATION', 5, 2, 0, 'LEGAL', 30, 0, 0, 'Send non-disclosure agreement to customer', 'system'),
(1, 'NDA Executed by Legal', 'CONFIRM', 'CONFIRMATION', 6, 2, 0, 'LEGAL', 480, 0, 0, 'Legal review and execution of NDA', 'system'),
(1, 'NDA Completed', 'CONFIRM', 'CONFIRMATION', 7, 2, 0, 'LEGAL', 15, 0, 0, 'Mark NDA process as completed', 'system');
(1, 'NDA End', 'END', 'COMPLETION', 7, 2, 0, 'SYSTEM', 15, 0, 1, 'NDA completed', 'system');
-- Task Flow for NDA Lane
EXEC sp_add_flow @from_name = 'Start NDA', @to_name = 'Start NDA', @condition = NULL;
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'Send NDA', @condition = NULL;
EXEC sp_add_flow @from_name = 'Send NDA', @to_name = 'NDA Executed by Legal', @condition = 'YES';
EXEC sp_add_flow @from_name = 'NDA Executed by Legal', @to_name = 'NDA Completed', @condition = 'YES';
EXEC sp_add_flow @from_name = 'Needs NDA', @to_name = 'NDA Completed', @condition = 'NO';
EXEC sp_add_flow @from_name = 'Needs Completed', @to_name = 'NDA End', @condition = 'NO';
EXEC sp_add_flow @from_name = 'NDA Completed', @to_name = 'NDA End', @condition = 'NO';
EXEC sp_add_flow @from_name = 'NDA End', @to_name = 'End', @condition = NULL;
-- Continue with other lanes...
-- Inspection Process Lane Tasks (LaneId = 3)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description)
VALUES
(1, 'Set Inspection Fee', 'USER', 'FINANCIAL', 8, 3, 0, 'INSP', 60, 1, 0, 'Calculate and set inspection fees'),
(1, 'Send KIM Invoice', 'USER', 'FINANCIAL', 9, 3, 0, 'BILLING', 30, 1, 0, 'Send Kosher Inspection and Monitoring invoice'),
(1, 'Payment Overdue - Escalation Required', 'USER', 'ESCALATION', 10, 3, 0, 'BILLING', 60, 0, 0, 'Handle overdue payment escalation'),
(1, 'Assign RFR', 'USER', 'ASSIGNMENT', 11, 3, 0, 'INSP', 30, 1, 0, 'Assign Regional Field Representative'),
(1, 'RFR Assigned', 'USER', 'CONFIRMATION', 12, 3, 0, 'RFR', 15, 1, 0, 'Confirm RFR assignment'),
(1, 'EIR Received/Reviewed', 'USER', 'REVIEW', 13, 3, 0, 'INSP', 240, 1, 0, 'Review Equipment Ingredient Report'),
(1, 'Notify IAR of EIR', 'SYSTEM', 'NOTIFICATION', 14, 3, 0, 'SYSTEM', 5, 1, 1, 'Notify IAR team of EIR completion');

-- Ingredients Review Lane Tasks (LaneId = 4)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description)
VALUES
(1, 'Assign to RC IAR Review', 'USER', 'ASSIGNMENT', 15, 4, 0, 'IAR_MANAGER', 15, 1, 0, 'Assign to Regional Coordinator for IAR review'),
(1, 'Schedule A Verification', 'USER', 'SCHEDULING', 16, 4, 0, 'IAR', 60, 1, 0, 'Schedule ingredient verification process'),
(1, 'Kosher Code Verification', 'USER', 'VERIFICATION', 17, 4, 0, 'IAR', 180, 1, 0, 'Verify kosher status codes for ingredients'),
(1, 'Supplier Approval Check', 'USER', 'VERIFICATION', 18, 4, 0, 'IAR', 120, 1, 0, 'Check supplier approvals and certifications'),
(1, 'Approved by IAR RC Review', 'USER', 'APPROVAL', 19, 4, 0, 'RC', 60, 1, 0, 'Regional Coordinator approval of IAR review'),
(1, 'IAR Completed', 'USER', 'COMPLETION', 20, 4, 0, 'RC', 15, 1, 0, 'Mark IAR process as completed');

-- Products Department Lane Tasks (LaneId = 5)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description)
VALUES
(1, 'Assign to Products Dept', 'USER', 'ASSIGNMENT', 21, 5, 0, 'PROD_MANAGER', 15, 1, 0, 'Assign application to Products Department'),
(1, 'Send PLA Invoice', 'USER', 'FINANCIAL', 22, 5, 0, 'BILLING', 30, 0, 0, 'Send Private Label Agreement invoice'),
(1, 'PLA Invoice Paid', 'USER', 'FINANCIAL', 23, 5, 0, 'BILLING', 15, 0, 0, 'Confirm PLA invoice payment'),
(1, 'Products Dept Complete', 'USER', 'COMPLETION', 24, 5, 0, 'PROD', 15, 1, 0, 'Mark Products Department review as completed');

-- Contract Processing Lane Tasks (LaneId = 6)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description)
VALUES
(1, 'Assign to RC', 'USER', 'ASSIGNMENT', 25, 6, 0, 'RC_MANAGER', 15, 1, 0, 'Assign to Regional Coordinator for contract review'),
(1, 'Review Completed by RC', 'USER', 'REVIEW', 26, 6, 0, 'RC', 180, 1, 0, 'Regional Coordinator completes final review'),
(1, 'Send Certification Contract', 'USER', 'COMMUNICATION', 27, 6, 0, 'RC', 45, 1, 0, 'Send certification contract to customer'),
(1, 'Contract Completed by Company', 'USER', 'APPROVAL', 28, 6, 0, 'RC', 30, 1, 0, 'Process completed contract from company');

-- Certification Lane Tasks (LaneId = 7)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description)
VALUES
(1, 'Send KCM Invoice', 'USER', 'FINANCIAL', 29, 7, 0, 'BILLING', 30, 1, 0, 'Send Kosher Certification and Monitoring invoice'),
(1, 'KCM Paid', 'USER', 'FINANCIAL', 30, 7, 0, 'BILLING', 15, 1, 0, 'Confirm KCM invoice payment'),
(1, 'Issue Certification', 'USER', 'COMPLETION', 31, 7, 0, 'CERT', 60, 1, 0, 'Issue final kosher certification');

-- =============================================
-- 4. TaskFlow Inserts
-- =============================================
-- Note: TaskId values are assumed based on the sequence above (1-31)
-- In a real scenario, you would need to query the TaskDefinitions table to get actual TaskIds

-- From Evaluate Application (TaskId = 1)
INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
VALUES
(1, 2, NULL, 1), -- Evaluate Application -> Assign to Products
(1, 3, NULL, 0), -- Evaluate Application -> Assign to IAR
(1, 4, NULL, 0); -- Evaluate Application -> Contact Customer

-- NDA Processing Flow
INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
VALUES
(5, 6, NULL, 1), -- Send NDA -> NDA Executed by Legal
(6, 7, NULL, 1); -- NDA Executed by Legal -> NDA Completed

-- Inspection Process Flow
INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
VALUES
(8, 9, NULL, 1),   -- Set Inspection Fee -> Send KIM Invoice
(10, 11, NULL, 1), -- Payment Overdue -> Assign RFR
(11, 12, NULL, 1), -- Assign RFR -> RFR Assigned
(12, 13, NULL, 1), -- RFR Assigned -> EIR Received/Reviewed
(13, 14, NULL, 1); -- EIR Received/Reviewed -> Notify IAR of EIR

-- Products Department Flow
INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
VALUES
(2, 21, NULL, 1),  -- Assign to Products -> Assign to Products Dept
(22, 23, NULL, 1), -- Send PLA Invoice -> PLA Invoice Paid
(23, 24, NULL, 1); -- PLA Invoice Paid -> Products Dept Complete

-- Ingredients Review Flow
INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
VALUES
(3, 15, NULL, 1),  -- Assign to IAR -> Assign to RC IAR Review
(15, 16, NULL, 1), -- Assign to RC IAR Review -> Schedule A Verification
(16, 17, NULL, 1), -- Schedule A Verification -> Kosher Code Verification
(17, 18, NULL, 1), -- Kosher Code Verification -> Supplier Approval Check
(18, 19, NULL, 1), -- Supplier Approval Check -> Approved by IAR RC Review
(19, 20, NULL, 1); -- Approved by IAR RC Review -> IAR Completed

-- Contract Processing Flow
INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
VALUES
(25, 26, NULL, 1), -- Assign to RC -> Review Completed by RC
(26, 27, NULL, 1), -- Review Completed by RC -> Send Certification Contract
(27, 28, NULL, 1), -- Send Certification Contract -> Contract Completed by Company
(28, 29, NULL, 1); -- Contract Completed by Company -> Send KCM Invoice

-- Certification Flow
INSERT INTO TaskFlow (FromTaskId, ToTaskId, Condition, IsDefault)
VALUES
(29, 30, NULL, 1), -- Send KCM Invoice -> KCM Paid
(30, 31, NULL, 1); -- KCM Paid -> Issue Certification
GO
-- =============================================
-- STORED PROCEDURES
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
    SET NOCOUNT ON;
    
    DECLARE @from_task_id INT = NULL;
    DECLARE @to_task_id INT;
    DECLARE @error_msg NVARCHAR(500);
    
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

-- Example usage:
-- EXEC sp_add_flow @from_name = 'Application Received', @to_name = 'Initial Review', @condition = NULL;
-- EXEC sp_add_flow @from_name = NULL, @to_name = 'Application Received', @condition = NULL; -- Start flow
-- EXEC sp_add_flow @from_name = 'Review Completed', @to_name = 'Send Approval', @condition = 'status = ''approved''';