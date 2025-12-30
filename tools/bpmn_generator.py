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
        self.stages = {}
        self.task_types = {}
        self.assignee_roles = {}
        
    def parse_sql_file(self, sql_content: str):
        """Parse the SQL file and extract tasks and flows"""
        
        # Extract stage information from comments
        stage_pattern = r'-- Stage: ([^(]+)\(ID: (\d+)\)'
        stage_matches = re.findall(stage_pattern, sql_content)
        
        for stage_name, stage_id in stage_matches:
            self.stages[int(stage_id)] = stage_name.strip()
        
        logger.info(f"Found {len(self.stages)} stages: {self.stages}")
        
        # Extract task definitions
        task_pattern = r"\(\d+,\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*\d+,\s*(\d+),\s*'([^']+)',\s*[^,]*,\s*'([^']*)',\s*[01],\s*'[^']*'\)"
        task_matches = re.findall(task_pattern, sql_content)
        
        for match in task_matches:
            task_name, task_type, task_category, stage_id, assignee_role, description = match
            self.tasks.append({
                'name': task_name,
                'type': task_type,
                'category': task_category,
                'stage_id': int(stage_id),
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
            'STAGESTART': 'startEvent',
            'STAGGEEND': 'endEvent'
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
        
        # Create stages
        stage_set = ET.SubElement(process, 'bpmn:stageSet')
        stage_elements = {}
        
        for stage_id, stage_name in self.stages.items():
            stage = ET.SubElement(stage_set, 'bpmn:stage')
            stage.set('id', f'Stage_{stage_id}')
            stage.set('name', stage_name)
            stage_elements[stage_id] = stage
        
        # Create tasks and events
        task_elements = {}
        
        for task in self.tasks:
            task_name = task['name']
            task_type = task['type']
            stage_id = task['stage_id']
            
            # Determine BPMN element type
            bpmn_type = self.get_bpmn_element_type(task_type)
            
            # Create element
            element_id = f"Task_{task_name.replace(' ', '_').replace('/', '_')}"
            element = ET.SubElement(process, f'bpmn:{bpmn_type}')
            element.set('id', element_id)
            element.set('name', task_name)
            
            # Add to stage
            if stage_id in stage_elements:
                flow_node_ref = ET.SubElement(stage_elements[stage_id], 'bpmn:flowNodeRef')
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
        
        pstage = ET.SubElement(diagram, 'bpmndi:BPMNPstage')
        pstage.set('id', 'BPMNPstage_1')
        pstage.set('bpmnElement', 'ApplicationCertification')
        
        # Add basic shapes (simplified positioning)
        x, y = 100, 100
        stage_height = 200
        task_width, task_height = 100, 80
        
        for stage_id, stage_name in self.stages.items():
            # Stage shape
            stage_shape = ET.SubElement(pstage, 'bpmndi:BPMNShape')
            stage_shape.set('id', f'Stage_{stage_id}_di')
            stage_shape.set('bpmnElement', f'Stage_{stage_id}')
            stage_shape.set('isHorizontal', 'true')
            
            bounds = ET.SubElement(stage_shape, 'dc:Bounds')
            bounds.set('x', '50')
            bounds.set('y', str(y))
            bounds.set('width', '1200')
            bounds.set('height', str(stage_height))
            
            # Tasks in this stage
            stage_tasks = [t for t in self.tasks if t['stage_id'] == stage_id]
            task_x = 150
            
            for i, task in enumerate(stage_tasks):
                task_id = f"Task_{task['name'].replace(' ', '_').replace('/', '_')}"
                task_shape = ET.SubElement(pstage, 'bpmndi:BPMNShape')
                task_shape.set('id', f'{task_id}_di')
                task_shape.set('bpmnElement', task_id)
                
                task_bounds = ET.SubElement(task_shape, 'dc:Bounds')
                task_bounds.set('x', str(task_x))
                task_bounds.set('y', str(y + 60))
                task_bounds.set('width', str(task_width))
                task_bounds.set('height', str(task_height))
                
                task_x += 120
            
            y += stage_height + 20
        
        # Convert to string
        rough_string = ET.tostring(definitions, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid flowchart syntax"""
        
        lines = ["flowchart TD"]
        lines.append("    %% Application Certification Workflow")
        lines.append("")
        
        # Add subgraphs for each stage
        for stage_id, stage_name in self.stages.items():
            lines.append(f"    subgraph Stage{stage_id} [\"{stage_name}\"]")
            
            # Add tasks in this stage
            stage_tasks = [t for t in self.tasks if t['stage_id'] == stage_id]
            for task in stage_tasks:
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
        
        # Stage summary
        report.append("## Workflow Stages (Swimstages)")
        for stage_id, stage_name in sorted(self.stages.items()):
            stage_tasks = [t for t in self.tasks if t['stage_id'] == stage_id]
            report.append(f"**{stage_name} (Stage {stage_id})**")
            report.append(f"- Tasks: {len(stage_tasks)}")
            report.append(f"- Roles: {', '.join(set(t['assignee_role'] for t in stage_tasks))}")
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
        
        # Detailed task list by stage
        report.append("## Detailed Task Breakdown")
        for stage_id, stage_name in sorted(self.stages.items()):
            report.append(f"### {stage_name}")
            stage_tasks = [t for t in self.tasks if t['stage_id'] == stage_id]
            
            for task in sorted(stage_tasks, key=lambda x: x['name']):
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
            'total_stages': len(generator.stages),
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