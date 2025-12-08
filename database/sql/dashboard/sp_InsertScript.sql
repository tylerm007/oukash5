-- Stored Procedure: Insert/Update Script for Task Definition
-- Usage: EXEC sp_InsertScript @task_name = 'Review Application', @script = '{"action": "validate", "fields": ["company", "contact"]}'

IF OBJECT_ID('dbo.sp_InsertScript', 'P') IS NOT NULL
    DROP PROCEDURE dbo.sp_InsertScript
GO

CREATE PROCEDURE dbo.sp_InsertScript
    @task_name NVARCHAR(255),
    @script NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @task_count INT;
    DECLARE @task_id INT;
    DECLARE @updated_rows INT;
    
    -- Validate required parameters
    IF @task_name IS NULL OR LEN(TRIM(@task_name)) = 0
    BEGIN
        RAISERROR('Parameter @task_name is required and cannot be empty', 16, 1);
        RETURN -1;
    END
    
    -- Validate script parameter (can be empty but not null)
    IF @script IS NULL
    BEGIN
        SET @script = '{}'; -- Default to empty JSON object
    END
    
    -- Check if the task name exists and get count
    SELECT @task_count = COUNT(*), @task_id = MIN(TaskId)
    FROM TaskDefinitions 
    WHERE TaskName = @task_name;
    
    -- Handle different scenarios
    IF @task_count = 0
    BEGIN
        -- Task not found
        SELECT 
            'ERROR' as Status,
            'Task not found' as Message,
            @task_name as TaskName,
            0 as TasksFound,
            0 as TasksUpdated;
        RETURN -2;
    END
    ELSE IF @task_count = 1
    BEGIN
        -- Single task found - update it
        UPDATE TaskDefinitions 
        SET 
            PostScriptJson = @script,
            ModifiedDate = GETDATE()
        WHERE TaskName = @task_name;
        
        SET @updated_rows = @@ROWCOUNT;
        
        SELECT 
            'SUCCESS' as Status,
            'Task script updated successfully' as Message,
            @task_name as TaskName,
            @task_count as TasksFound,
            @updated_rows as TasksUpdated,
            @task_id as TaskId,
            @script as UpdatedScript;
    END
    ELSE
    BEGIN
        -- Multiple tasks found with same name - update all
        UPDATE TaskDefinitions 
        SET 
            PostScriptJson = @script,
            ModifiedDate = GETDATE()
        WHERE TaskName = @task_name;
        
        SET @updated_rows = @@ROWCOUNT;
        
        SELECT 
            'WARNING' as Status,
            'Multiple tasks found with same name - all updated' as Message,
            @task_name as TaskName,
            @task_count as TasksFound,
            @updated_rows as TasksUpdated,
            @script as UpdatedScript;
    END
    
    RETURN 0;
END
GO

-- Grant permissions (adjust as needed)
-- GRANT EXECUTE ON dbo.sp_InsertScript TO [your_app_user]
GO

-- Example usage and test cases:
/*
-- Test 1: Update existing task with JSON script
EXEC sp_InsertScript 
    @task_name = 'Review Application',
    @script = '{"action": "validate", "fields": ["company", "contact"], "required": true}';

-- Test 2: Update task with simple script
EXEC sp_InsertScript 
    @task_name = 'Approve Contract',
    @script = '{"approval_level": "manager", "auto_notify": true}';

-- Test 3: Clear script (set to empty JSON)
EXEC sp_InsertScript 
    @task_name = 'Send Email',
    @script = '{}';

-- Test 4: Test with non-existent task (should return error)
EXEC sp_InsertScript 
    @task_name = 'NonExistentTask',
    @script = '{"test": "value"}';

-- Test 5: Test with null script (should default to {})
EXEC sp_InsertScript 
    @task_name = 'Review Application',
    @script = NULL;

-- View results to verify updates
SELECT TaskId, TaskName, PostScriptJson, ModifiedDate 
FROM TaskDefinitions 
WHERE TaskName IN ('Review Application', 'Approve Contract', 'Send Email')
ORDER BY TaskName;
*/