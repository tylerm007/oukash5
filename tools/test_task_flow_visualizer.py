"""
Test script for TaskFlow Visualizer
Demonstrates how to use the TaskFlowGraph class to visualize workflows
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.task_flow_visualizer import TaskFlowGraph, create_task_flow_from_database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_manual_graph():
    """Example of creating a task flow graph manually"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Manual Task Flow Creation")
    print("="*60 + "\n")
    
    # Create a simple workflow
    graph = TaskFlowGraph("Sample Approval Workflow")
    
    # Add nodes
    graph.add_node("Start Application", "START")
    graph.add_node("Submit Form", "ACTION")
    graph.add_node("Manager Review", "ACTION")
    graph.add_node("Approval Decision", "CONDITION")
    graph.add_node("Process Payment", "ACTION")
    graph.add_node("Send Rejection", "ACTION")
    graph.add_node("Notify Applicant", "ACTION")
    graph.add_node("End Process", "END")
    
    # Add flows
    graph.add_flow("Start Application", "Submit Form")
    graph.add_flow("Submit Form", "Manager Review")
    graph.add_flow("Manager Review", "Approval Decision")
    graph.add_flow("Approval Decision", "Process Payment", condition="Approved")
    graph.add_flow("Approval Decision", "Send Rejection", condition="Rejected")
    graph.add_flow("Process Payment", "Notify Applicant")
    graph.add_flow("Send Rejection", "Notify Applicant")
    graph.add_flow("Notify Applicant", "End Process")
    
    # Display statistics
    stats = graph.get_statistics()
    print(f"Process: {stats['process_name']}")
    print(f"Total Nodes: {stats['total_nodes']}")
    print(f"Total Edges: {stats['total_edges']}")
    print(f"Conditional Flows: {stats['conditional_flows']}")
    print(f"\nTask Types: {stats['task_types']}")
    
    # Validate
    issues = graph.validate_flow()
    if issues:
        print("\n⚠️  Validation Issues:")
        for issue in issues:
            print(f"  [{issue['severity'].upper()}] {issue['message']}")
    else:
        print("\n✅ Flow validation passed!")
    
    return graph


def example_mermaid_output(graph: TaskFlowGraph):
    """Example of generating Mermaid diagram"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Mermaid Diagram Output")
    print("="*60 + "\n")
    
    mermaid = graph.generate_mermaid_diagram()
    print(mermaid)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'sample_workflow.mmd')
    with open(output_file, 'w') as f:
        f.write(mermaid)
    print(f"\n✅ Mermaid diagram saved to: {output_file}")


def example_dot_output(graph: TaskFlowGraph):
    """Example of generating DOT/Graphviz diagram"""
    print("\n" + "="*60)
    print("EXAMPLE 3: DOT/Graphviz Output")
    print("="*60 + "\n")
    
    dot = graph.generate_dot_diagram()
    print(dot)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'sample_workflow.dot')
    with open(output_file, 'w') as f:
        f.write(dot)
    print(f"\n✅ DOT diagram saved to: {output_file}")
    print(f"   To render: dot -Tpng {output_file} -o sample_workflow.png")


def example_ascii_output(graph: TaskFlowGraph):
    """Example of generating ASCII text diagram"""
    print("\n" + "="*60)
    print("EXAMPLE 4: ASCII Text Diagram")
    print("="*60 + "\n")
    
    ascii_diagram = graph.generate_ascii_diagram()
    print(ascii_diagram)


def example_html_output(graph: TaskFlowGraph):
    """Example of generating HTML visualization"""
    print("\n" + "="*60)
    print("EXAMPLE 5: HTML Interactive Diagram")
    print("="*60 + "\n")
    
    html = graph.export_to_html(include_mermaid=True)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'sample_workflow.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ HTML diagram saved to: {output_file}")
    print(f"   Open in browser to view interactive diagram")


def example_from_database():
    """Example of loading task flow from database"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Load from Database")
    print("="*60 + "\n")
    
    try:
        # This requires a running database connection
        import safrs
        from database import models
        
        db = safrs.DB
        session = db.session
        
        # Example process name - change this to match your database
        process_name = "OU Application Init"
        
        print(f"Loading process: {process_name}")
        graph = create_task_flow_from_database(session, process_name)
        
        stats = graph.get_statistics()
        print(f"\n✅ Loaded from database:")
        print(f"   Total Nodes: {stats['total_nodes']}")
        print(f"   Total Edges: {stats['total_edges']}")
        
        # Generate HTML output
        html = graph.export_to_html(include_mermaid=True)
        output_file = os.path.join(os.path.dirname(__file__), f'{process_name.replace(" ", "_")}_flow.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n✅ HTML diagram saved to: {output_file}")
        
        return graph
        
    except Exception as e:
        print(f"⚠️  Could not load from database: {e}")
        print("   Make sure the application server is configured and database is accessible")
        return None


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("TaskFlow Visualizer - Examples and Tests")
    print("="*60)
    
    # Example 1: Create manual graph
    graph = example_manual_graph()
    
    # Example 2-5: Different output formats
    example_mermaid_output(graph)
    example_dot_output(graph)
    example_ascii_output(graph)
    example_html_output(graph)
    
    # Example 6: Load from database (if available)
    # Uncomment if you want to try database loading
    # example_from_database()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
