
# User Documentation for workflow.py

"""
## Overview
The workflow.py module is responsible for managing workflow-related operations in the application. It provides functionality to interact with workflows, including starting new workflows, managing tasks, and logging workflow history.

## Key Functions

### start_workflow
This function starts a new workflow instance based on the provided process name, application ID, and user details.

#### Parameters:
- process_name (str): The name of the workflow process to start.
- application_id (str): The ID of the application associated with the workflow.
- started_by (str): The user who initiated the workflow.
- priority (str, optional): The priority of the workflow. Defaults to 'Normal'.

#### Returns:
- str: The unique identifier of the newly created workflow instance.

#### Example Usage:
    instance_id = start_workflow(
        process_name="Onboarding",
        application_id="APP12345",
        started_by="admin_user",
        priority="High"
    )
    print(f"Workflow started with Instance ID: {instance_id}")

## Dependencies
This module relies on the following libraries:
- pyodbc: For database connectivity and executing SQL queries.
- uuid: For generating unique identifiers.

## Notes
- Ensure the database connection string is correctly configured in the pyodbc.connect call.
- Proper error handling is implemented to raise exceptions when the process definition is not found.

## Future Enhancements
- Add support for additional workflow actions such as pausing, resuming, and terminating workflows.
- Implement logging for better traceability of workflow operations.
"""
## /complete_task
### Method: POST, OPTIONS

Description
Marks a task in the workflow as completed.

Request Body
'''
task_instance_id (string): ID of the task instance to complete.
completed_by (string): User who completed the task.
completion_notes (string, optional): Notes about the task completion.
Response
200 OK: Returns the task_instance_id of the completed task.
404 Not Found: If the task instance or task definition is not found.
400 Bad Request: If prior tasks are not completed.
'''
## /application_message
### Method: POST, OPTIONS

Description
Sends a message related to an application in the workflow.

Request Body
'''
message (string): The message text.
application_id (string): ID of the application.
from_user (string): Sender of the message.
to_user (string): Recipient of the message.
priority (string, optional): Priority of the message. Default is "NORMAL".
message_type (string, optional): Type of the message. Default is "Standard".
Response
200 OK: Returns the application_id of the application.
404 Not Found: If the application is not found.
'''

## /process_message
### Method: POST, OPTIONS

Description
Sends a message related to a process in the workflow.

Request Body
'''
message (string): The message text.
process_id (string): ID of the process.
from_user (string): Sender of the message.
to_user (string): Recipient of the message.
subject (string): Subject of the message.
priority (string, optional): Priority of the message. Default is "NORMAL".
message_type (string, optional): Type of the message. Default is "Standard".
Response
200 OK: Returns the process_id of the process.
404 Not Found: If the process instance is not found.
'''
## /assign_task
### Method: POST, OPTIONS

Description
Assigns a user to a task in the workflow.

Request Body
''''
task_instance_id (string): ID of the task instance.
user_id (string): ID of the user to assign.
Response
200 OK: Returns the task_instance_id of the task.
404 Not Found: If the task instance is not found.
Notes
All endpoints log their operations for debugging and traceability.
Ensure the database models and relationships are correctly configured for the endpoints to function properly.
Proper error handling is implemented to return meaningful error messages.
'''