"""
Simple BPMN Generator Test
"""

import os
import re

def parse_sql_and_generate_mermaid():
    """Parse SQL file and generate Mermaid diagram"""
    
    sql_file = "database/sql/task_definitions.sql"
    
    if not os.path.exists(sql_file):
        print(f"❌ File not found: {sql_file}")
        return
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✅ SQL file loaded")
    
    # Extract lanes from comments
    lanes = {}
    lane_pattern = r'-- Lane: ([^(]+)\(ID: (\d+)\)'
    for match in re.finditer(lane_pattern, content):
        lane_name = match.group(1).strip()
        lane_id = int(match.group(2))
        lanes[lane_id] = lane_name
    
    print(f"🏊 Found {len(lanes)} lanes: {list(lanes.values())}")
    
    # Extract tasks
    tasks = []
    task_pattern = r"\(\d+,\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*\d+,\s*(\d+),\s*'([^']+)',\s*[^,]*,\s*'([^']*)',\s*[01],\s*'[^']*'\)"
    
    for match in re.finditer(task_pattern, content):
        task_name = match.group(1)
        task_type = match.group(2)
        task_category = match.group(3)
        lane_id = int(match.group(4))
        assignee_role = match.group(5)
        description = match.group(6)
        
        tasks.append({
            'name': task_name,
            'type': task_type,
            'category': task_category,
            'lane_id': lane_id,
            'assignee_role': assignee_role,
            'description': description
        })
    
    print(f"🎯 Found {len(tasks)} tasks")
    
    # Extract flows
    flows = []
    flow_pattern = r"sp_add_flow @from_name = '([^']+)', @to_name = '([^']+)', @condition = '([^']*)'"
    
    for match in re.finditer(flow_pattern, content):
        from_task = match.group(1)
        to_task = match.group(2)
        condition = match.group(3)
        
        flows.append({
            'from': from_task,
            'to': to_task,
            'condition': condition if condition != 'None' else ''
        })
    
    print(f"➡️ Found {len(flows)} flows")
    
    # Generate Mermaid diagram
    mermaid_lines = ["flowchart TD"]
    mermaid_lines.append("    %% Application Certification Workflow")
    mermaid_lines.append("")
    
    # Add subgraphs for lanes
    for lane_id, lane_name in sorted(lanes.items()):
        mermaid_lines.append(f"    subgraph Lane{lane_id}[\"{lane_name}\"]")
        
        # Add tasks in this lane
        lane_tasks = [t for t in tasks if t['lane_id'] == lane_id]
        for task in lane_tasks:
            task_id = task['name'].replace(' ', '_').replace('/', '_').replace('-', '_')
            task_type = task['type']
            
            # Choose shape based on task type
            if task_type == 'START':
                shape = f"(({task['name']}))"
            elif task_type == 'END':
                shape = f"([{task['name']}])"
            elif task_type in ['CONDITION']:
                shape = f"{{{task['name']}}}"
            elif task_type == 'GATEWAY':
                shape = f"{{{{{task['name']}}}}}"
            else:
                shape = f"[{task['name']}]"
            
            mermaid_lines.append(f"        {task_id}{shape}")
        
        mermaid_lines.append("    end")
        mermaid_lines.append("")
    
    # Add flows
    mermaid_lines.append("    %% Sequence Flows")
    for flow in flows:
        from_id = flow['from'].replace(' ', '_').replace('/', '_').replace('-', '_')
        to_id = flow['to'].replace(' ', '_').replace('/', '_').replace('-', '_')
        condition = flow['condition']
        
        if condition:
            mermaid_lines.append(f"    {from_id} -->|{condition}| {to_id}")
        else:
            mermaid_lines.append(f"    {from_id} --> {to_id}")
    
    # Add styling
    mermaid_lines.append("")
    mermaid_lines.append("    %% Styling")
    mermaid_lines.append("    classDef startEnd fill:#90EE90,stroke:#333,stroke-width:2px")
    mermaid_lines.append("    classDef userTask fill:#87CEEB,stroke:#333,stroke-width:2px")
    mermaid_lines.append("    classDef gateway fill:#FFD700,stroke:#333,stroke-width:2px")
    mermaid_lines.append("    classDef condition fill:#FFA500,stroke:#333,stroke-width:2px")
    
    mermaid_content = "\n".join(mermaid_lines)
    
    # Create output directory
    os.makedirs("docs/workflow_diagrams", exist_ok=True)
    
    # Write Mermaid file
    with open("docs/workflow_diagrams/workflow.mmd", 'w', encoding='utf-8') as f:
        f.write(mermaid_content)
    
    # Create HTML viewer
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Application Certification Workflow</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .diagram {{ text-align: center; margin: 20px 0; }}
        .info {{ background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #007acc; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .stat-card {{ background: #f0f8ff; padding: 15px; border-radius: 8px; text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #007acc; }}
        h1 {{ color: #333; text-align: center; }}
        .mermaid {{ background: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 Application Certification Workflow</h1>
        
        <div class="info">
            <h3>📊 Workflow Overview</h3>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{len(tasks)}</div>
                    <div>Total Tasks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(flows)}</div>
                    <div>Process Flows</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(lanes)}</div>
                    <div>Swimlanes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(set(t['assignee_role'] for t in tasks))}</div>
                    <div>Roles</div>
                </div>
            </div>
        </div>
        
        <div class="diagram">
            <div class="mermaid">
{mermaid_content}
            </div>
        </div>
        
        <div class="info">
            <h3>🏊 Workflow Lanes</h3>
            <ul>
                {chr(10).join([f'<li><strong>{lane_name}:</strong> {len([t for t in tasks if t["lane_id"] == lane_id])} tasks</li>' for lane_id, lane_name in sorted(lanes.items())])}
            </ul>
        </div>
        
        <div class="info">
            <h3>👥 Roles Involved</h3>
            <ul>
                {chr(10).join([f'<li><strong>{role}:</strong> {len([t for t in tasks if t["assignee_role"] == role])} tasks</li>' for role in sorted(set(t["assignee_role"] for t in tasks))])}
            </ul>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true, 
            theme: 'default',
            flowchart: {{ useMaxWidth: true, htmlLabels: true }},
            securityLevel: 'loose'
        }});
    </script>
</body>
</html>"""
    
    with open("docs/workflow_diagrams/workflow_viewer.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n✅ BPMN diagram generation complete!")
    print(f"📁 Files created in docs/workflow_diagrams/:")
    print(f"   🔀 workflow.mmd - Mermaid diagram source")
    print(f"   🌐 workflow_viewer.html - Interactive viewer")
    print(f"\n🌐 Open workflow_viewer.html in your browser to view the diagram!")
    
    return True

if __name__ == "__main__":
    parse_sql_and_generate_mermaid()