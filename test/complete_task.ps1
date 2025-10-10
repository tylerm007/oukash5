

$body = @{
            task_instance_id = 102
            result = "Approved"
            completed_by = "user1"
            completion_notes = "Task completed successfully"
        } | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5656/complete_task" -Method POST -Body $body -ContentType "application/json"  -Headers @{
            Authorization = 'Bearer  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDEwOTE4NywianRpIjoiNzdmNWU0ZTgtMWExMi00YmE2LWI5OTktZGQ5NjQ2YTJiOTk1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzYwMTA5MTg3LCJleHAiOjE3NjAxMjI1MDd9.agBto0Y1mKyX6igWFb3YhUbiE22TYYeyaJyBqOc8VPQ'
}