"""
BPMN Diagram Generator from SQL Task Definitions
Parses task_definitions.sql and generates BPMN XML and visual representation
"""

import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Tuple, Set
import logging

logger = logging.getLogger(__name__)

class BPMNGenerator:
    """Generate BPMN diagrams from SQL task definitions"""
    
    def __init__(self):
        self.tasks = []
        self.flows = []
        self.lanes = {}
        self.task_types = {}
        self.assignee_roles = {}
        
    def parse_sql_file(self, sql_content: str):
        """Parse the SQL file and extract tasks and flows"""
        
        # Extract lane information from comments
        lane_pattern = r'-- Lane: ([^(]+)\(ID: (\d+)\)'
        lane_matches = re.findall(lane_pattern, sql_content)
        
        for lane_name, lane_id in lane_matches:
            self.lanes[int(lane_id)] = lane_name.strip()
        
        logger.info(f"Found {len(self.lanes)} lanes: {self.lanes}")
        
        # Extract task definitions
        task_pattern = r"\(\d+,\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*\d+,\s*(\d+),\s*'([^']+)',\s*[^,]*,\s*'([^']*)',\s*[01],\s*'[^']*'\)"
        task_matches = re.findall(task_pattern, sql_content)
        
        for match in task_matches:
            task_name, task_type, task_category, lane_id, assignee_role, description = match
            self.tasks.append({
                'name': task_name,
                'type': task_type,
                'category': task_category,
                'lane_id': int(lane_id),
                'assignee_role': assignee_role,
                'description': description
            })
            self.task_types[task_name] = task_type
            self.assignee_roles[task_name] = assignee_role
        
        logger.info(f"Found {len(self.tasks)} tasks")
        
        # Extract flows
        flow_pattern = r"sp_add_flow @from_name = '([^']+)', @to_name = '([^']+)', @condition = '([^']*)'"
        flow_matches = re.findall(flow_pattern, sql_content)
        
        for from_task, to_task, condition in flow_matches:
            self.flows.append({
                'from': from_task,
                'to': to_task,
                'condition': condition if condition != 'None' else ''
            })
        
        logger.info(f"Found {len(self.flows)} flows")
    
    def get_bpmn_element_type(self, task_type: str) -> str:
        """Map SQL task type to BPMN element type"""
        mapping = {
            'START': 'startEvent',
            'END': 'endEvent',
            'ACTION': 'userTask',
            'CONFIRM': 'userTask',
            'CONDITION': 'exclusiveGateway',
            'GATEWAY': 'parallelGateway',
            'LANESTART': 'startEvent',
            'LANEEND': 'endEvent'
        }
        return mapping.get(task_type, 'task')
    
    def generate_bpmn_xml(self) -> str:
        """Generate BPMN 2.0 XML"""
        
        # Create root elements
        definitions = ET.Element('bpmn:definitions')
        definitions.set('xmlns:bpmn', 'http://www.omg.org/spec/BPMN/20100524/MODEL')
        definitions.set('xmlns:bpmndi', 'http://www.omg.org/spec/BPMN/20100524/DI')
        definitions.set('xmlns:dc', 'http://www.omg.org/spec/DD/20100524/DC')
        definitions.set('xmlns:di', 'http://www.omg.org/spec/DD/20100524/DI')
        definitions.set('id', 'ApplicationCertificationProcess')
        definitions.set('targetNamespace', 'http://bpmn.io/schema/bpmn')
        
        # Create process
        process = ET.SubElement(definitions, 'bpmn:process')
        process.set('id', 'ApplicationCertification')
        process.set('isExecutable', 'true')
        
        # Create lanes
        lane_set = ET.SubElement(process, 'bpmn:laneSet')
        lane_elements = {}
        
        for lane_id, lane_name in self.lanes.items():
            lane = ET.SubElement(lane_set, 'bpmn:lane')
            lane.set('id', f'Lane_{lane_id}')
            lane.set('name', lane_name)
            lane_elements[lane_id] = lane
        
        # Create tasks and events
        task_elements = {}
        
        for task in self.tasks:
            task_name = task['name']
            task_type = task['type']
            lane_id = task['lane_id']
            
            # Determine BPMN element type
            bpmn_type = self.get_bpmn_element_type(task_type)
            
            # Create element
            element_id = f"Task_{task_name.replace(' ', '_').replace('/', '_')}"
            element = ET.SubElement(process, f'bpmn:{bpmn_type}')
            element.set('id', element_id)
            element.set('name', task_name)
            
            # Add to lane
            if lane_id in lane_elements:
                flow_node_ref = ET.SubElement(lane_elements[lane_id], 'bpmn:flowNodeRef')
                flow_node_ref.text = element_id
            
            # Add assignee for user tasks
            if bpmn_type == 'userTask':
                assignee = task['assignee_role']
                if assignee != 'SYSTEM':
                    performer = ET.SubElement(element, 'bpmn:performer')
                    performer.set('name', assignee)
            
            # Add documentation
            if task['description']:
                documentation = ET.SubElement(element, 'bpmn:documentation')
                documentation.text = task['description']
            
            task_elements[task_name] = element_id
        
        # Create sequence flows
        flow_id_counter = 1
        
        for flow in self.flows:
            from_task = flow['from']
            to_task = flow['to']
            condition = flow['condition']
            
            if from_task in task_elements and to_task in task_elements:
                flow_element = ET.SubElement(process, 'bpmn:sequenceFlow')
                flow_id = f'Flow_{flow_id_counter}'
                flow_element.set('id', flow_id)
                flow_element.set('sourceRef', task_elements[from_task])
                flow_element.set('targetRef', task_elements[to_task])
                
                if condition:
                    flow_element.set('name', condition)
                    # Add condition expression for gateways
                    if condition in ['YES', 'NO']:
                        condition_expr = ET.SubElement(flow_element, 'bpmn:conditionExpression')
                        condition_expr.set('xsi:type', 'bpmn:tFormalExpression')
                        condition_expr.text = f'${{{condition.lower()}}}'
                
                flow_id_counter += 1
        
        # Create diagram (basic positioning)
        diagram = ET.SubElement(definitions, 'bpmndi:BPMNDiagram')
        diagram.set('id', 'BPMNDiagram_1')
        
        plane = ET.SubElement(diagram, 'bpmndi:BPMNPlane')
        plane.set('id', 'BPMNPlane_1')
        plane.set('bpmnElement', 'ApplicationCertification')
        
        # Add basic shapes (simplified positioning)
        x, y = 100, 100
        lane_height = 200
        task_width, task_height = 100, 80
        
        for lane_id, lane_name in self.lanes.items():
            # Lane shape
            lane_shape = ET.SubElement(plane, 'bpmndi:BPMNShape')
            lane_shape.set('id', f'Lane_{lane_id}_di')
            lane_shape.set('bpmnElement', f'Lane_{lane_id}')
            lane_shape.set('isHorizontal', 'true')
            
            bounds = ET.SubElement(lane_shape, 'dc:Bounds')
            bounds.set('x', '50')
            bounds.set('y', str(y))
            bounds.set('width', '1200')
            bounds.set('height', str(lane_height))
            
            # Tasks in this lane
            lane_tasks = [t for t in self.tasks if t['lane_id'] == lane_id]
            task_x = 150
            
            for i, task in enumerate(lane_tasks):
                task_id = f"Task_{task['name'].replace(' ', '_').replace('/', '_')}"
                task_shape = ET.SubElement(plane, 'bpmndi:BPMNShape')
                task_shape.set('id', f'{task_id}_di')
                task_shape.set('bpmnElement', task_id)
                
                task_bounds = ET.SubElement(task_shape, 'dc:Bounds')
                task_bounds.set('x', str(task_x))
                task_bounds.set('y', str(y + 60))
                task_bounds.set('width', str(task_width))
                task_bounds.set('height', str(task_height))
                
                task_x += 120
            
            y += lane_height + 20
        
        # Convert to string
        rough_string = ET.tostring(definitions, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid flowchart syntax"""
        
        lines = ["flowchart TD"]
        lines.append("    %% Application Certification Workflow")
        lines.append("")
        
        # Add subgraphs for each lane
        for lane_id, lane_name in self.lanes.items():
            lines.append(f"    subgraph Lane{lane_id} [\"{lane_name}\"]")
            
            # Add tasks in this lane
            lane_tasks = [t for t in self.tasks if t['lane_id'] == lane_id]
            for task in lane_tasks:
                task_id = task['name'].replace(' ', '_').replace('/', '_')
                task_type = task['type']
                
                # Choose shape based on task type
                if task_type == 'START':
                    shape = f"({task['name']})"
                elif task_type == 'END':
                    shape = f"([{task['name']}])"
                elif task_type in ['CONDITION', 'GATEWAY']:
                    shape = f"{{{task['name']}}}"
                else:
                    shape = f"[{task['name']}]"
                
                lines.append(f"        {task_id}{shape}")
            
            lines.append("    end")
            lines.append("")
        
        # Add flows
        lines.append("    %% Sequence Flows")
        for flow in self.flows:
            from_id = flow['from'].replace(' ', '_').replace('/', '_')
            to_id = flow['to'].replace(' ', '_').replace('/', '_')
            condition = flow['condition']
            
            if condition:
                lines.append(f"    {from_id} -->|{condition}| {to_id}")
            else:
                lines.append(f"    {from_id} --> {to_id}")
        
        # Add styling
        lines.append("")
        lines.append("    %% Styling")
        lines.append("    classDef startEnd fill:#90EE90")
        lines.append("    classDef userTask fill:#87CEEB")
        lines.append("    classDef gateway fill:#FFD700")
        lines.append("    classDef condition fill:#FFA500")
        
        # Apply styles
        for task in self.tasks:
            task_id = task['name'].replace(' ', '_').replace('/', '_')
            task_type = task['type']
            
            if task_type in ['START', 'END', 'LANESTART', 'LANEEND']:
                lines.append(f"    class {task_id} startEnd")
            elif task_type in ['ACTION', 'CONFIRM']:
                lines.append(f"    class {task_id} userTask")
            elif task_type == 'GATEWAY':
                lines.append(f"    class {task_id} gateway")
            elif task_type == 'CONDITION':
                lines.append(f"    class {task_id} condition")
        
        return "\n".join(lines)
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of the workflow"""
        
        report = []
        report.append("# Application Certification Workflow Analysis")
        report.append("=" * 50)
        report.append("")
        
        # Lane summary
        report.append("## Workflow Lanes (Swimlanes)")
        for lane_id, lane_name in sorted(self.lanes.items()):
            lane_tasks = [t for t in self.tasks if t['lane_id'] == lane_id]
            report.append(f"**{lane_name} (Lane {lane_id})**")
            report.append(f"- Tasks: {len(lane_tasks)}")
            report.append(f"- Roles: {', '.join(set(t['assignee_role'] for t in lane_tasks))}")
            report.append("")
        
        # Task type summary
        report.append("## Task Types Distribution")
        type_counts = {}
        for task in self.tasks:
            task_type = task['type']
            type_counts[task_type] = type_counts.get(task_type, 0) + 1
        
        for task_type, count in sorted(type_counts.items()):
            report.append(f"- {task_type}: {count} tasks")
        report.append("")
        
        # Role distribution
        report.append("## Role Assignments")
        role_counts = {}
        for task in self.tasks:
            role = task['assignee_role']
            role_counts[role] = role_counts.get(role, 0) + 1
        
        for role, count in sorted(role_counts.items()):
            report.append(f"- {role}: {count} tasks")
        report.append("")
        
        # Critical path analysis
        report.append("## Workflow Paths")
        
        # Find start and end tasks
        start_tasks = [t['name'] for t in self.tasks if t['type'] == 'START']
        end_tasks = [t['name'] for t in self.tasks if t['type'] == 'END']
        
        report.append(f"- Start Points: {', '.join(start_tasks)}")
        report.append(f"- End Points: {', '.join(end_tasks)}")
        report.append(f"- Total Flows: {len(self.flows)}")
        
        # Conditional flows
        conditional_flows = [f for f in self.flows if f['condition']]
        report.append(f"- Conditional Flows: {len(conditional_flows)}")
        report.append("")
        
        # Detailed task list by lane
        report.append("## Detailed Task Breakdown")
        for lane_id, lane_name in sorted(self.lanes.items()):
            report.append(f"### {lane_name}")
            lane_tasks = [t for t in self.tasks if t['lane_id'] == lane_id]
            
            for task in sorted(lane_tasks, key=lambda x: x['name']):
                report.append(f"**{task['name']}** ({task['type']})")
                report.append(f"- Role: {task['assignee_role']}")
                report.append(f"- Category: {task['category']}")
                if task['description']:
                    report.append(f"- Description: {task['description']}")
                
                # Find incoming/outgoing flows
                incoming = [f for f in self.flows if f['to'] == task['name']]
                outgoing = [f for f in self.flows if f['from'] == task['name']]
                
                if incoming:
                    report.append(f"- Incoming: {', '.join([f'{f[\"from\"]}' + (f' ({f[\"condition\"]})' if f['condition'] else '') for f in incoming])}")
                if outgoing:
                    report.append(f"- Outgoing: {', '.join([f'{f[\"to\"]}' + (f' ({f[\"condition\"]})' if f['condition'] else '') for f in outgoing])}")
                
                report.append("")
        
        return "\n".join(report)


def generate_bpmn_from_sql(sql_file_path: str = None, sql_content: str = None):
    """Main function to generate BPMN from SQL file"""
    
    generator = BPMNGenerator()
    
    # Read SQL content
    if sql_content:
        content = sql_content
    elif sql_file_path:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        raise ValueError("Either sql_file_path or sql_content must be provided")
    
    # Parse and generate
    generator.parse_sql_file(content)
    
    return {
        'bpmn_xml': generator.generate_bpmn_xml(),
        'mermaid': generator.generate_mermaid_diagram(),
        'summary': generator.generate_summary_report(),
        'stats': {
            'total_tasks': len(generator.tasks),
            'total_flows': len(generator.flows),
            'total_lanes': len(generator.lanes),
            'task_types': list(set(t['type'] for t in generator.tasks)),
            'roles': list(set(t['assignee_role'] for t in generator.tasks))
        }
    }


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        sql_file = sys.argv[1]
        result = generate_bpmn_from_sql(sql_file_path=sql_file)
        
        # Write outputs
        with open('workflow.bpmn', 'w', encoding='utf-8') as f:
            f.write(result['bpmn_xml'])
        
        with open('workflow.mmd', 'w', encoding='utf-8') as f:
            f.write(result['mermaid'])
        
        with open('workflow_analysis.md', 'w', encoding='utf-8') as f:
            f.write(result['summary'])
        
        print("Generated:")
        print("- workflow.bpmn (BPMN 2.0 XML)")
        print("- workflow.mmd (Mermaid diagram)")
        print("- workflow_analysis.md (Analysis report)")
        print(f"\nStats: {result['stats']}")
    else:
        print("Usage: python bpmn_generator.py <sql_file_path>")