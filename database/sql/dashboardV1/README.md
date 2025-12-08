# SQL Server Deployment

```
create database dashboardV1;
use dashboardV1;
```

## OU Application
The Application is the key table that links to the Legacy tables (CCOMPANYTB and PLANTTB).
```
Application.sql
```
![OU Application Schema](images/application_schema.png)
## BPMN Workflow model
The model defines Processes, Lanes, and Tasks - these are instantiated using http://{server}:{port}/start_workflow. UserRoles will be replaced with ou_kash tables in next revision.
```
BPMN_table_defs.sql
TaskInstances.sql
task_definitions.sql
UserRoles.sql
```
![OU Workflow Schema](images/bpmn_schema.png)

## Handy SQL Scripts

View all Task Instances 
```
use dashboardV1;
go

SELECT TOP (1000) [TaskInstanceId]
      ,ti.[TaskId]
      ,td.[TaskName]
      ,td.[TaskType]
      ,td.[AssigneeRole]
      ,[StageId]
      ,[Status]
      ,[AssignedTo]
      ,[StartedDate]
      ,[CompletedDate]
      ,td.[EstimatedDurationMinutes]
      ,[Result]
      ,[ResultData]
      ,[ErrorMessage]
      ,[RetryCount]
  FROM [dashboardV1].[dbo].[TaskInstances] ti,
  TaskDefinitions td
  where ti.TaskId = td.TaskId
```