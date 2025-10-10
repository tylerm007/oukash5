#!/bin/bash
# filepath: /Users/tylerband/OU/oukash5/test/complete_task.sh
# Bash wrapper for PowerShell complete_task script
# Usage: complete_task.sh <task_instance_id> [result] [completed_by] [notes]

# Check if at least one argument is provided
if [ $# -eq 0 ] || [ -z "$1" ]; then
    echo "Usage: $0 <task_instance_id> [result] [completed_by] [notes]"
    echo "Example: $0 104 \"COMPLETED\" \"tband\" \"Task COMPLETED\""
    exit 1
fi

TASK_ID="$1"
RESULT="${2:-Approved}"
COMPLETED_BY="${3:-user1}"
NOTES="${4:-Task completed successfully}"

echo "Completing task ID $TASK_ID..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#!/bin/bash
# filepath: /Users/tylerband/OU/oukash5/test/complete_task_wrapper.sh
# Bash wrapper script to complete a task with configurable parameters
# Usage: ./complete_task_wrapper.sh -t 104 [-r "Approved"] [-c "user1"] [-n "Task completed successfully"]

# Function to display usage
usage() {
    echo "Usage: $0 -t <task_instance_id> [-r result] [-c completed_by] [-n notes]"
    echo "  -t: Task Instance ID (required)"
    echo "  -r: Result (default: 'Approved')"
    echo "  -c: Completed By (default: 'user1')"
    echo "  -n: Notes (default: 'Task completed successfully')"
    echo ""
    echo "Example: $0 -t 104 -r \"COMPLETED\" -c \"tband\" -n \"Task COMPLETED\""
    exit 1
}

# Set defaults
RESULT="Approved"
COMPLETED_BY="user1"
NOTES="Task completed successfully"
TASK_INSTANCE_ID=""

# Parse command line arguments
while getopts "t:r:c:n:h" opt; do
    case $opt in
        t)
            TASK_INSTANCE_ID="$OPTARG"
            ;;
        r)
            RESULT="$OPTARG"
            ;;
        c)
            COMPLETED_BY="$OPTARG"
            ;;
        n)
            NOTES="$OPTARG"
            ;;
        h)
            usage
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
    esac
done

# Check if required parameter is provided
if [ -z "$TASK_INSTANCE_ID" ]; then
    echo "Error: Task Instance ID is required" >&2
    usage
fi

# Display parameters for confirmation
echo -e "\033[33mCompleting task with the following parameters:\033[0m"
echo -e "\033[36m  Task Instance ID: $TASK_INSTANCE_ID\033[0m"
echo -e "\033[36m  Result: $RESULT\033[0m"
echo -e "\033[36m  Completed By: $COMPLETED_BY\033[0m"
echo -e "\033[36m  Notes: $NOTES\033[0m"
echo ""

# Create the JSON request body
JSON_BODY=$(cat <<EOF
{
    "task_instance_id": $TASK_INSTANCE_ID,
    "result": "$RESULT",
    "completed_by": "$COMPLETED_BY",
    "completion_notes": "$NOTES"
}
EOF
)

# Make the API call
echo -e "\033[32mSending request to complete task...\033[0m"

RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDEwOTE4NywianRpIjoiNzdmNWU0ZTgtMWExMi00YmE2LWI5OTktZGQ5NjQ2YTJiOTk1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzYwMTA5MTg3LCJleHAiOjE3NjAxMjI1MDd9.agBto0Y1mKyX6igWFb3YhUbiE22TYYeyaJyBqOc8VPQ" \
    -d "$JSON_BODY" \
    "http://localhost:5656/complete_task")

# Extract HTTP status code and body
HTTP_STATUS=$(echo "$RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
HTTP_BODY=$(echo "$RESPONSE" | sed -e 's/HTTPSTATUS:.*//g')

# Check if the request was successful
if [ "$HTTP_STATUS" -eq 200 ]; then
    echo -e "\033[32mTask completed successfully!\033[0m"
    echo -e "\033[37mResponse: $HTTP_BODY\033[0m"
else
    echo -e "\033[31mError completing task:\033[0m"
    echo -e "\033[31mHTTP Status: $HTTP_STATUS\033[0m"
    echo -e "\033[31mResponse: $HTTP_BODY\033[0m"
    exit 1
fi