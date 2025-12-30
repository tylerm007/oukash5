"""
Simple TaskFlow Visualization Example
Copy and run this to quickly visualize your workflow
"""

# Example 1: Using the REST API (easiest method)
# ==============================================
# Just run this in PowerShell while your server is running:

'''
# Get HTML visualization
Invoke-RestMethod -Uri "http://localhost:5656/visualize_task_flow?process_name=OU Application Init&format=html" -Method GET -OutFile "my_workflow.html"

# Then open my_workflow.html in your browser!
'''

# Example 2: Using Python code
# =============================
if __name__ == "__main__":
    import sys
    import os
    
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from tools.task_flow_visualizer import create_task_flow_from_database
    import safrs
    
    # Initialize database
    try:
        db = safrs.DB
        session = db.session
        
        # CHANGE THIS to your process name
        PROCESS_NAME = "OU Application Init"
        
        print(f"Loading workflow: {PROCESS_NAME}")
        
        # Load workflow from database
        graph = create_task_flow_from_database(session, PROCESS_NAME)
        
        # Get statistics
        stats = graph.get_statistics()
        print(f"\n✅ Loaded workflow:")
        print(f"   Total Tasks: {stats['total_nodes']}")
        print(f"   Total Flows: {stats['total_edges']}")
        print(f"   Task Types: {stats['task_types']}")
        
        # Validate
        issues = graph.validate_flow()
        if issues:
            print(f"\n⚠️  Found {len(issues)} validation issues:")
            for issue in issues:
                print(f"   [{issue['severity']}] {issue['message']}")
        else:
            print("\n✅ Workflow validation passed!")
        
        # Generate HTML
        html = graph.export_to_html(include_mermaid=True)
        output_file = f"{PROCESS_NAME.replace(' ', '_')}_flow.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n✅ HTML diagram saved to: {output_file}")
        print(f"   Open this file in your browser to view the interactive diagram")
        
        # Also generate Mermaid for markdown
        mermaid = graph.generate_mermaid_diagram()
        mermaid_file = f"{PROCESS_NAME.replace(' ', '_')}_flow.mmd"
        with open(mermaid_file, 'w', encoding='utf-8') as f:
            f.write(mermaid)
        print(f"\n✅ Mermaid diagram saved to: {mermaid_file}")
        print(f"   Use this in markdown files or GitHub")
        
        # Print ASCII preview
        print("\n" + "="*60)
        print("ASCII Preview:")
        print("="*60)
        print(graph.generate_ascii_diagram())
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. Your API server is running")
        print("2. The process name is correct")
        print("3. You have database access configured")
        import traceback
        traceback.print_exc()
