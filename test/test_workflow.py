import requests

'''
select ti.TaskInstanceId, ti.TaskId,ti.Status, td.TaskName, td.TaskType from TaskInstances ti, TaskDefinitions td
where StageId =22 and ti.TaskId = td.TaskId
43	3	NEW	Start_Application_Submitted	START
44	4	NEW	AssignNCRC	ACTION
45	5	NEW	verify Company	CONFIRM
46	6	NEW	verify Plant	CONFIRM
47	7	NEW	verify Contact	CONFIRM
48	8	NEW	verify Product	CONFIRM
49	9	NEW	verify Ingredients	CONFIRM
50	10	NEW	All Verified Gateway	GATEWAY
51	11	NEW	to Withdrawn Y/N	CONDITION
52	12	NEW	Assign Product	CONFIRM
53	13	NEW	Assign Ingredients	CONFIRM
54	14	NEW	Contact Customer	CONFIRM
55	15	NEW	Initial Collector	GATEWAY
56	16	NEW	End	END
'''
def complete_task(task_id):
    url = f"http://localhost:5656/api/TaskInstance/{task_id}"
    payload = {
        "data": {
            "type": "TaskInstance",
            "id": task_id,
            "attributes": {
                "Status": "COMPLETED"
            }
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.patch(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"✅ TaskInstance with TaskId {task_id} updated successfully.")
        return response.json()['data']['id']  # Return the updated TaskInstanceId
    else:
        print(f"❌ Failed to update TaskInstance. Status Code: {response.status_code}, Response: {response.text}")
        return None

def test_get_api(task_id):
    
    response = requests.get(f"http://localhost:5656/api/TaskInstance/{task_id}")
    assert response.status_code == 200
    assert "data" in response.json()
    print(response.json())
    return response.json()

if __name__ == "__main__":
    task_id = 43
    complete_task(task_id)
    task_id = 44
    complete_task(task_id)
    response = test_get_api(task_id)
    task_id = 45
    complete_task(task_id)
    task_id = 46
    complete_task(task_id)
    task_id = 47
    complete_task(task_id)
    task_id = 48
    complete_task(task_id)