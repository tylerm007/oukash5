
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
('LANESTART','Subprocess Lane Start'),
('LANEEND','Subprocess Lane End'),
('PROGRESS', 'Subprocess Progress'),
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
('INPUT', 'Data Input and Entry'),
('SELECTOR', 'Selection and Decision Making'),
('SUBPROCESS','Internal processing only'),
('PROGRESS_TASK', 'Subprocess Progress'),
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
('NEW', 'New Task Created'),
('ON_HOLD', 'Task On Hold'),    
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


-- Insert Process Definition and Tasks
-- =============================================

-- =============================================
-- 1. ProcessDefinition Insert
-- =============================================


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
-- =============================================
-- 3. StageDefinitions Inserts
-- =============================================
INSERT INTO StageDefinitions (ProcessId, StageName, StageDescription, EstimatedDurationDays, CreatedBy)
VALUES
(1, 'Initial', 'Initial application review and task assignment', 2, 'system'),
(1, 'NDA', 'Non-disclosure agreement handling and execution', 3, 'system'),
(1, 'Inspection', 'Plant inspection and RFR assignment process', 10, 'system'),
(1, 'Ingredients', 'IAR ingredients and kosher code review process', 7, 'system'),
(1, 'Products', 'Product evaluation and PLA processing', 5, 'system'),
(1, 'Contract', 'Contract review and certification agreement', 3, 'system'),
(1, 'Certification', 'Final certification and invoice processing', 2, 'system');
GO
-- 
-- =============================================
-- 4. TaskFlow Inserts
-- =============================================
-- Note: TaskId values are assumed based on the sequence above (1-31)
-- In a real scenario, you would need to query the TaskDefinitions table to get actual TaskIds

-- RUN task_definitions.sql

-- Example usage:
-- EXEC sp_add_flow @from_name = 'Application Received', @to_name = 'Initial Review', @condition = NULL;
-- EXEC sp_add_flow @from_name = NULL, @to_name = 'Application Received', @condition = NULL; -- Start flow
-- EXEC sp_add_flow @from_name = 'Review Completed', @to_name = 'Send Approval', @condition = 'status = ''approved''';