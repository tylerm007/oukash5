@echo off
REM Batch wrapper for PowerShell complete_task script
REM Usage: complete_task.cmd <task_instance_id> [result] [completed_by] [notes]

if "%~1"=="" (
    echo Usage: %0 ^<task_instance_id^> [result] [completed_by] [notes]
    echo Example: %0 104 "COMPLETED" "tband" "Task COMPLETED"
    exit /b 1
)

set TASK_ID=%1
set RESULT=%~2
set COMPLETED_BY=%~3
set NOTES=%~4

REM Set defaults if not provided
if "%RESULT%"=="" set RESULT=""
if "%COMPLETED_BY%"=="" set COMPLETED_BY=tband
if "%NOTES%"=="" set NOTES=Task completed successfully

echo Completing task ID %TASK_ID%...

powershell -ExecutionPolicy Bypass -File "%~dp0complete_task_wrapper.ps1" -TaskInstanceId %TASK_ID% -Result "%RESULT%" -CompletedBy "%COMPLETED_BY%" -Notes "%NOTES%"