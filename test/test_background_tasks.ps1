# Test Background Task Execution
# This script demonstrates how to use the new async task completion endpoints

# Configuration
$baseUrl = "https://localhost:5656"
$token = "YOUR_JWT_TOKEN_HERE"  # Replace with actual token

# Example 1: Submit a task for background processing
Write-Host "=== Example 1: Submit Background Task ===" -ForegroundColor Cyan

$body = @{
    task_instance_id = 454  # Replace with actual task instance ID
    result = "Approved"
    completed_by = "admin"
    capacity = "ADMIN"
    completion_notes = "Task completed via background processing"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod `
        -Uri "$baseUrl/complete_task_async" `
        -Method POST `
        -Body $body `
        -ContentType "application/json" `
        -Headers @{Authorization = "Bearer $token"} `
        -SkipCertificateCheck  # For self-signed certs
    
    Write-Host "✅ Task submitted successfully!" -ForegroundColor Green
    Write-Host "Task ID: $($response.task_id)"
    Write-Host "Check status at: $($response.check_status_url)"
    
    $taskId = $response.task_id
    
} catch {
    Write-Host "❌ Error submitting task: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Example 2: Poll for task completion
Write-Host "=== Example 2: Poll for Task Status ===" -ForegroundColor Cyan

$maxWaitSeconds = 300  # 5 minutes max
$pollInterval = 2      # Start with 2 seconds
$maxInterval = 30      # Max 30 seconds between polls
$elapsedTime = 0

Write-Host "Waiting for task to complete (max $maxWaitSeconds seconds)..."

while ($elapsedTime -lt $maxWaitSeconds) {
    try {
        $status = Invoke-RestMethod `
            -Uri "$baseUrl/task_script_status/$taskId" `
            -Method GET `
            -Headers @{Authorization = "Bearer $token"} `
            -SkipCertificateCheck
        
        $statusEmoji = switch ($status.status) {
            "pending" { "⏳" }
            "running" { "🔄" }
            "completed" { "✅" }
            "failed" { "❌" }
            default { "❓" }
        }
        
        Write-Host "$statusEmoji Status: $($status.status) (elapsed: ${elapsedTime}s)" -NoNewline
        
        if ($status.status -eq "running" -and $status.started_at) {
            $started = [DateTime]::Parse($status.started_at)
            $runTime = ([DateTime]::Now - $started).TotalSeconds
            Write-Host " - Running for: $([Math]::Round($runTime, 1))s"
        } else {
            Write-Host ""
        }
        
        # Check if task is complete
        if ($status.status -notin @("pending", "running")) {
            Write-Host ""
            if ($status.status -eq "completed") {
                Write-Host "🎉 Task completed successfully!" -ForegroundColor Green
                Write-Host "Duration: $($status.duration_seconds) seconds"
                Write-Host "Result:" -ForegroundColor Yellow
                Write-Host ($status.result | ConvertTo-Json -Depth 5)
            } else {
                Write-Host "💥 Task failed!" -ForegroundColor Red
                Write-Host "Error: $($status.error)"
            }
            break
        }
        
        # Wait before next poll (exponential backoff)
        Start-Sleep -Seconds $pollInterval
        $elapsedTime += $pollInterval
        $pollInterval = [Math]::Min($pollInterval * 1.5, $maxInterval)
        
    } catch {
        Write-Host "❌ Error checking status: $_" -ForegroundColor Red
        break
    }
}

if ($elapsedTime -ge $maxWaitSeconds) {
    Write-Host "⏰ Timeout waiting for task completion" -ForegroundColor Yellow
    Write-Host "Task is still running. Check status later with:"
    Write-Host "  GET $baseUrl/task_script_status/$taskId"
}

Write-Host ""

# Example 3: Fire and forget (submit without waiting)
Write-Host "=== Example 3: Fire and Forget ===" -ForegroundColor Cyan

$body2 = @{
    task_instance_id = 455  # Different task
    result = "Pending Review"
    completed_by = "admin"
    capacity = "ADMIN"
} | ConvertTo-Json

try {
    $response2 = Invoke-RestMethod `
        -Uri "$baseUrl/complete_task_async" `
        -Method POST `
        -Body $body2 `
        -ContentType "application/json" `
        -Headers @{Authorization = "Bearer $token"} `
        -SkipCertificateCheck
    
    Write-Host "✅ Task submitted (fire and forget)" -ForegroundColor Green
    Write-Host "Task ID: $($response2.task_id)"
    Write-Host "You can check status later at: $($response2.check_status_url)"
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Tips:"
Write-Host "  - Use background tasks for operations > 30 seconds"
Write-Host "  - Implement polling with exponential backoff"
Write-Host "  - Store task_id for later status checks"
Write-Host "  - Handle both success and failure cases"
Write-Host ""
Write-Host "📚 See docs/background_task_execution_guide.md for more info"
