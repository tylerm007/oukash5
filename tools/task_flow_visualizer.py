"""
TaskFlow Visualizer
Generates visual diagrams of workflow task flows using TaskDefinition.TaskName
Supports multiple output formats: Mermaid, DOT/Graphviz, and ASCII
"""

from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class TaskFlowNode:
    """Represents a single node in the task flow"""
    
    def __init__(self, task_name: str, task_type: str = None, task_id: int = None):
        self.task_name = task_name
        self.task_type = task_type or "ACTION"
        self.task_id = task_id
        self.incoming_flows: List['TaskFlowEdge'] = []
        self.outgoing_flows: List['TaskFlowEdge'] = []
    
    def __repr__(self):
        return f"TaskFlowNode({self.task_name}, type={self.task_type})"
    
    def __hash__(self):
        return hash(self.task_name)
    
    def __eq__(self, other):
        if isinstance(other, TaskFlowNode):
            return self.task_name == other.task_name
        return False


class TaskFlowEdge:
    """Represents a flow connection between two tasks"""
    
    def __init__(self, from_node: TaskFlowNode, to_node: TaskFlowNode, condition: str = None, is_default: bool = False):
        self.from_node = from_node
        self.to_node = to_node
        self.condition = condition
        self.is_default = is_default
    
    def __repr__(self):
        cond = f", condition='{self.condition}'" if self.condition else ""
        return f"TaskFlowEdge({self.from_node.task_name} -> {self.to_node.task_name}{cond})"


class TaskFlowGraph:
    """
    Main class for modeling and visualizing task flows
    Uses TaskDefinition.TaskName to create flow diagrams
    """
    
    def __init__(self, process_name: str = "Workflow Process"):
        self.process_name = process_name
        self.nodes: Dict[str, TaskFlowNode] = {}
        self.edges: List[TaskFlowEdge] = []
        self.start_nodes: Set[TaskFlowNode] = set()
        self.end_nodes: Set[TaskFlowNode] = set()
    
    def add_node(self, task_name: str, task_type: str = None, task_id: int = None) -> TaskFlowNode:
        """Add a task node to the graph"""
        if task_name not in self.nodes:
            node = TaskFlowNode(task_name, task_type, task_id)
            self.nodes[task_name] = node
            
            # Track start and end nodes
            if task_type == 'START':
                self.start_nodes.add(node)
            elif task_type == 'END':
                self.end_nodes.add(node)
            
            logger.info(f"Added node: {task_name} (type: {task_type})")
        return self.nodes[task_name]
    
    def add_flow(self, from_task: str, to_task: str, condition: str = None, is_default: bool = False):
        """Add a flow connection between two tasks"""
        from_node = self.nodes.get(from_task)
        to_node = self.nodes.get(to_task)
        
        if not from_node or not to_node:
            logger.warning(f"Cannot add flow: {from_task} -> {to_task}. Node(s) not found.")
            return
        
        edge = TaskFlowEdge(from_node, to_node, condition, is_default)
        self.edges.append(edge)
        from_node.outgoing_flows.append(edge)
        to_node.incoming_flows.append(edge)
        
        logger.info(f"Added flow: {from_task} -> {to_task}" + (f" (condition: {condition})" if condition else ""))
    
    def load_from_database(self, session):
        """
        Load task flow data from database
        
        Args:
            session: SQLAlchemy database session
        """
        from database.models import TaskDefinition, TaskFlow, ProcessDefinition
        
        # Get process definition
        process_def = session.query(ProcessDefinition).filter_by(ProcessName=self.process_name, IsActive=True).first()
        if not process_def:
            logger.error(f"Process definition not found: {self.process_name}")
            return False
        
        # Load all tasks for the process
        task_defs = session.query(TaskDefinition).filter_by(ProcessDefinitionId=process_def.ProcessId).all()
        
        for task_def in task_defs:
            self.add_node(
                task_name=task_def.TaskName,
                task_type=task_def.TaskType,
                task_id=task_def.TaskId
            )
        
        # Load all flows
        task_flows = session.query(TaskFlow).join(
            TaskDefinition, TaskFlow.ToTaskId == TaskDefinition.TaskId
        ).filter(
            TaskDefinition.ProcessDefinitionId == process_def.ProcessId
        ).all()
        
        for flow in task_flows:
            from_task_name = flow.FromTask.TaskName if flow.FromTask else None
            to_task_name = flow.ToTask.TaskName if flow.ToTask else None
            
            if from_task_name and to_task_name:
                self.add_flow(
                    from_task=from_task_name,
                    to_task=to_task_name,
                    condition=flow.Condition,
                    is_default=flow.IsDefault
                )
        
        logger.info(f"Loaded {len(self.nodes)} nodes and {len(self.edges)} edges from database")
        return True
    
    def get_node_shape(self, node: TaskFlowNode) -> Tuple[str, str]:
        """
        Get the appropriate shape for a node based on its type
        Returns tuple of (mermaid_shape, dot_shape)
        """
        shapes = {
            'START': ('((', '))', 'circle'),
            'END': ('((', '))', 'doublecircle'),
            'CONDITION': ('{{', '}}', 'diamond'),
            'GATEWAY': ('{{', '}}', 'diamond'),
            'ACTION': ('[', ']', 'box'),
            'CONFIRM': ('[', ']', 'box'),
        }
        
        mermaid_open, mermaid_close, dot_shape = shapes.get(
            node.task_type, ('[', ']', 'box')
        )
        return (mermaid_open, mermaid_close), dot_shape
    
    def generate_mermaid_diagram(self) -> str:
        """
        Generate a Mermaid flowchart diagram
        
        Returns:
            str: Mermaid diagram syntax
        """
        lines = ["flowchart TD"]
        lines.append(f"    %% {self.process_name}")
        lines.append("")
        
        # Define nodes with appropriate shapes
        node_ids = {}
        for idx, (task_name, node) in enumerate(self.nodes.items()):
            node_id = f"N{idx}"
            node_ids[task_name] = node_id
            
            (open_char, close_char), _ = self.get_node_shape(node)
            
            # Escape special characters in task name
            safe_name = task_name.replace('"', '\\"')
            lines.append(f"    {node_id}{open_char}\"{safe_name}\"{close_char}")
        
        lines.append("")
        lines.append("    %% Flow connections")
        
        # Add edges
        for edge in self.edges:
            from_id = node_ids[edge.from_node.task_name]
            to_id = node_ids[edge.to_node.task_name]
            
            if edge.condition:
                # Conditional flow with label
                safe_condition = edge.condition.replace('"', '\\"')
                lines.append(f"    {from_id} -->|{safe_condition}| {to_id}")
            else:
                # Regular flow
                lines.append(f"    {from_id} --> {to_id}")
        
        return "\n".join(lines)
    
    def generate_dot_diagram(self) -> str:
        """
        Generate a Graphviz DOT diagram
        
        Returns:
            str: DOT diagram syntax
        """
        lines = ["digraph TaskFlow {"]
        lines.append(f"    label=\"{self.process_name}\";")
        lines.append("    rankdir=TB;")
        lines.append("    node [style=filled, fillcolor=lightblue];")
        lines.append("")
        
        # Define nodes
        node_ids = {}
        for idx, (task_name, node) in enumerate(self.nodes.items()):
            node_id = f"N{idx}"
            node_ids[task_name] = node_id
            
            _, dot_shape = self.get_node_shape(node)
            
            # Escape special characters
            safe_name = task_name.replace('"', '\\"')
            
            # Set color based on type
            color = {
                'START': 'lightgreen',
                'END': 'lightcoral',
                'CONDITION': 'lightyellow',
                'GATEWAY': 'lightyellow',
            }.get(node.task_type, 'lightblue')
            
            lines.append(f'    {node_id} [label="{safe_name}", shape={dot_shape}, fillcolor={color}];')
        
        lines.append("")
        
        # Add edges
        for edge in self.edges:
            from_id = node_ids[edge.from_node.task_name]
            to_id = node_ids[edge.to_node.task_name]
            
            if edge.condition:
                safe_condition = edge.condition.replace('"', '\\"')
                lines.append(f'    {from_id} -> {to_id} [label="{safe_condition}"];')
            else:
                lines.append(f'    {from_id} -> {to_id};')
        
        lines.append("}")
        return "\n".join(lines)
    
    def generate_ascii_diagram(self) -> str:
        """
        Generate a simple ASCII text representation of the flow
        
        Returns:
            str: ASCII diagram
        """
        lines = [f"=== {self.process_name} ===\n"]
        
        # Group nodes by incoming flow count (for simple topological ordering)
        visited = set()
        
        def print_node_recursive(node: TaskFlowNode, indent: int = 0):
            if node.task_name in visited:
                return
            visited.add(node.task_name)
            
            prefix = "  " * indent
            type_marker = {
                'START': '[START]',
                'END': '[END]',
                'CONDITION': '<COND>',
                'GATEWAY': '<GATE>',
            }.get(node.task_type, '')
            
            lines.append(f"{prefix}{type_marker} {node.task_name}")
            
            for edge in node.outgoing_flows:
                condition_str = f" [if: {edge.condition}]" if edge.condition else ""
                lines.append(f"{prefix}  |{condition_str}")
                lines.append(f"{prefix}  v")
                print_node_recursive(edge.to_node, indent + 1)
        
        # Start from start nodes
        for start_node in self.start_nodes:
            print_node_recursive(start_node)
        
        return "\n".join(lines)
    
    def get_statistics(self) -> Dict:
        """Get statistics about the task flow"""
        return {
            'process_name': self.process_name,
            'total_nodes': len(self.nodes),
            'total_edges': len(self.edges),
            'start_nodes': len(self.start_nodes),
            'end_nodes': len(self.end_nodes),
            'conditional_flows': sum(1 for e in self.edges if e.condition),
            'task_types': {
                task_type: sum(1 for n in self.nodes.values() if n.task_type == task_type)
                for task_type in set(n.task_type for n in self.nodes.values())
            }
        }
    
    def validate_flow(self) -> List[Dict]:
        """
        Validate the task flow for common issues
        
        Returns:
            List of validation errors/warnings
        """
        issues = []
        
        # Check for orphaned nodes (except START)
        for node in self.nodes.values():
            if node.task_type != 'START' and len(node.incoming_flows) == 0:
                issues.append({
                    'severity': 'error',
                    'node': node.task_name,
                    'message': f"Task '{node.task_name}' has no incoming flows"
                })
            
            if node.task_type != 'END' and len(node.outgoing_flows) == 0:
                issues.append({
                    'severity': 'error',
                    'node': node.task_name,
                    'message': f"Task '{node.task_name}' has no outgoing flows"
                })
        
        # Check for missing start/end nodes
        if not self.start_nodes:
            issues.append({
                'severity': 'error',
                'node': None,
                'message': "No START nodes found in the flow"
            })
        
        if not self.end_nodes:
            issues.append({
                'severity': 'warning',
                'node': None,
                'message': "No END nodes found in the flow"
            })
        
        return issues
    
    def export_to_html(self, include_mermaid: bool = True) -> str:
        """
        Generate an HTML file with embedded diagram visualization
        
        Args:
            include_mermaid: Whether to include Mermaid.js rendering
        
        Returns:
            str: HTML content
        """
        mermaid_diagram = self.generate_mermaid_diagram() if include_mermaid else ""
        stats = self.get_statistics()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.process_name} - Task Flow</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .stats {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .stats h2 {{
            margin-top: 0;
            color: #555;
        }}
        .stat-item {{
            display: inline-block;
            margin: 5px 15px;
            padding: 5px 10px;
            background-color: #e3f2fd;
            border-radius: 3px;
        }}
        .diagram {{
            margin: 20px 0;
            padding: 20px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .mermaid {{
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{self.process_name}</h1>
        
        <div class="stats">
            <h2>Flow Statistics</h2>
            <div class="stat-item"><strong>Total Tasks:</strong> {stats['total_nodes']}</div>
            <div class="stat-item"><strong>Total Flows:</strong> {stats['total_edges']}</div>
            <div class="stat-item"><strong>Start Nodes:</strong> {stats['start_nodes']}</div>
            <div class="stat-item"><strong>End Nodes:</strong> {stats['end_nodes']}</div>
            <div class="stat-item"><strong>Conditional Flows:</strong> {stats['conditional_flows']}</div>
        </div>
        
        <div class="diagram">
            <h2>Task Flow Diagram</h2>
            <div class="mermaid">
{mermaid_diagram}
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>"""
        return html


def create_task_flow_from_database(session, process_name: str) -> TaskFlowGraph:
    """
    Helper function to create a TaskFlowGraph from database
    
    Args:
        session: SQLAlchemy database session
        process_name: Name of the process to visualize
    
    Returns:
        TaskFlowGraph instance
    """
    graph = TaskFlowGraph(process_name)
    graph.load_from_database(session)
    return graph


# Example usage
if __name__ == "__main__":
    # This would typically be run from a Flask endpoint or script
    print("TaskFlow Visualizer - Use create_task_flow_from_database() to generate diagrams")
