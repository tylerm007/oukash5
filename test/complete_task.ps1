

$body = @{
            task_instance_id = 102
            result = "Approved"
            completed_by = "user1"
            completion_notes = "Task completed successfully"
        } | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5656/complete_task" -Method POST -Body $body -ContentType "application/json"