# PowerShell wrapper script to complete a task with configurable parameters
# Usage: .\complete_task_wrapper.ps1 -TaskInstanceId 104 [-Result "Approved"] [-CompletedBy "user1"] [-Notes "Task completed successfully"]

param(
    [Parameter(Mandatory=$true)]
    [int]$TaskInstanceId,
    
    [Parameter(Mandatory=$false)]
    [string]$Result = "Approved",
    
    [Parameter(Mandatory=$false)]
    [string]$CompletedBy = "user1",
    
    [Parameter(Mandatory=$false)]
    [string]$Notes = "Task completed successfully"
)

# Display parameters for confirmation
Write-Host "Completing task with the following parameters:" -ForegroundColor Yellow
Write-Host "  Task Instance ID: $TaskInstanceId" -ForegroundColor Cyan
Write-Host "  Result: $Result" -ForegroundColor Cyan
Write-Host "  Completed By: $CompletedBy" -ForegroundColor Cyan
Write-Host "  Notes: $Notes" -ForegroundColor Cyan
Write-Host ""

# Create the request body
$body = @{
    task_instance_id = $TaskInstanceId
    result = $Result
    completed_by = $CompletedBy
    completion_notes = $Notes
} | ConvertTo-Json

try {
    # Make the API call
    Write-Host "Sending request to complete task..." -ForegroundColor Green
    $response = Invoke-RestMethod -Uri "http://localhost:5656/complete_task" -Method POST -Body $body -ContentType "application/json"
    # "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDEwOTE4NywianRpIjoiNzdmNWU0ZTgtMWExMi00YmE2LWI5OTktZGQ5NjQ2YTJiOTk1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzYwMTA5MTg3LCJleHAiOjE3NjAxMjI1MDd9.agBto0Y1mKyX6igWFb3YhUbiE22TYYeyaJyBqOc8VPQ
    # Display success message
    Write-Host "Task completed successfully!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor White
    
} catch {
    # Handle errors
    Write-Host "Error completing task:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        Write-Host "HTTP Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        Write-Host "Response Message: $($_.Exception.Response)" -ForegroundColor Red
    }
    exit 1
}