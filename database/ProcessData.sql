use dashboard;

    
-- =============================================
-- Additional Reference Data Inserts
-- =============================================

-- Lane Roles (if not already exist)
INSERT INTO LaneRoles (RoleCode, RoleDescription) VALUES
('NCRC', 'NCRC Coordinator'),
('LEGAL', 'Legal Department'),
('INSP', 'Inspection Team'),
('IAR', 'Ingredients Review Team'),
('PROD', 'Products Department'),
('RC', 'Regional Coordinator'),
('CERT', 'Certification Team'),
('BILLING', 'Billing Department'),
('IAR_MANAGER', 'IAR Manager'),
('PROD_MANAGER', 'Products Manager'),
('RC_MANAGER', 'RC Manager'),
('RFR', 'Regional Field Representative'),
('SYSTEM', 'System Automated');


-- Task Types
INSERT INTO TaskTypes (TaskTypeCode, TaskTypeDescription) VALUES
('USER', 'User Task - Requires human interaction'),
('SYSTEM', 'System Task - Automated execution'),
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
('CONFIRMATION', 'Confirmation and Verification'),
('NOTIFICATION', 'System Notifications'),
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


-- =============================================
-- Insert Process Definition and Tasks
-- =============================================

-- =============================================
-- 1. ProcessDefinition Insert
-- =============================================
INSERT INTO ProcessDefinitions (ProcessName, ProcessVersion, Description, IsActive, CreatedBy)
VALUES ('OU Certification Workflow', '1.0', 'Complete workflow for OU Kosher certification process', 1, 'system');

-- =============================================
-- 2. LaneDefinition Inserts
-- =============================================
INSERT INTO LaneDefinitions (ProcessId, LaneName, LaneDescription, EstimatedDurationDays, LaneRole, CreatedBy)
VALUES 
(1, 'Initial Processing', 'Initial application review and task assignment', 2, 'NCRC', 'system'),
(1, 'NDA Processing', 'Non-disclosure agreement handling and execution', 3, 'LEGAL', 'system'),
(1, 'Inspection Process', 'Plant inspection and RFR assignment process', 10, 'INSP', 'system'),
(1, 'Ingredients Review', 'IAR ingredients and kosher code review process', 7, 'IAR', 'system'),
(1, 'Products Department', 'Product evaluation and PLA processing', 5, 'PROD', 'system'),
(1, 'Contract Processing', 'Contract review and certification agreement', 3, 'RC', 'system'),
(1, 'Certification', 'Final certification and invoice processing', 2, 'CERT', 'system');



-- Insert Task Definitions for Admin Completion Workflow
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, AssigneeRole, EstimatedDurationMinutes, Description, AutoComplete)
VALUES 
    (1, 'Start_Application_Submitted', 'Event', 'Start', 1, 1, 'System', NULL, 'Application submitted and ready for admin review', 1),
    (1, 'Mark_Application_Complete', 'UserTask', 'Action', 10, 1, 'Admin', 2, 'Admin marks application as complete and ready for dispatch', 0),
    (1, 'Admin_Action_Gateway', 'Gateway', 'Decision', 11, 1, 'Admin', NULL, 'Admin chooses next action: Dispatch, Undo, Comment, or Message', 0),
    (1, 'Dispatch_To_Queue', 'ServiceTask', 'Action', 12, 1, 'Admin', 1, 'Send application to dispatcher review queue', 0),
    (1, 'Undo_Completion', 'UserTask', 'Action', 13, 1, 'Admin', 1, 'Return application to incomplete status for further review', 0),
    (1, 'Add_Internal_Comment', 'UserTask', 'Notification', 14, 1, 'Admin', 3, 'Add internal comment for audit trail', 0),
    (1, 'Send_Message_To_Dispatcher', 'UserTask', 'Notification', 15, 1, 'Admin', 5, 'Send message to dispatcher about application status', 0),
    (1, 'Application_Dispatched', 'Event', 'End', 16, 1, 'System', NULL, 'Application successfully dispatched to review queue', 1),
    (1, 'Under_Review', 'Event', 'End', 17, 1, 'Dispatcher', NULL, 'Application is under review by dispatcher', 1);


-- =============================================
-- 3. TaskDefinition Inserts
-- =============================================
-- Initial Processing Lane Tasks (LaneId = 1)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description)
VALUES
(1, 'Evaluate Application', 'USER', 'REVIEW', 1, 1, 0, 'NCRC', 120, 1, 0, 'Initial evaluation of certification application'),
(1, 'Assign to Products', 'USER', 'ASSIGNMENT', 2, 1, 1, 'NCRC', 15, 1, 0, 'Assign application to Products Department'),
(1, 'Assign to IAR', 'USER', 'ASSIGNMENT', 3, 1, 1, 'NCRC', 15, 1, 0, 'Assign application to Ingredients Review'),
(1, 'Contact Customer', 'USER', 'COMMUNICATION', 4, 1, 1, 'NCRC', 30, 1, 0, 'Initial customer contact for information gathering');

-- NDA Processing Lane Tasks (LaneId = 2)
INSERT INTO TaskDefinitions (ProcessId, TaskName, TaskType, TaskCategory, Sequence, LaneId, IsParallel, AssigneeRole, EstimatedDurationMinutes, IsRequired, AutoComplete, Description)
VALUES
(1, 'Send NDA', 'USER', 'COMMUNICATION', 5, 2, 0, 'LEGAL', 30, 0, 0, 'Send non-disclosure agreement to customer'),
(1, 'NDA Executed by Legal', 'USER', 'APPROVAL', 6, 2, 0, 'LEGAL', 480, 0, 0, 'Legal review and execution of NDA'),
(1, 'NDA Completed', 'USER', 'COMPLETION', 7, 2, 0, 'LEGAL', 15, 0, 0, 'Mark NDA process as completed');

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