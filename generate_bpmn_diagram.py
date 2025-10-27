"""
Generate BPMN Diagram from task_definitions.sql
Creates visual workflow diagrams from your SQL workflow definition
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.bpmn_generator import generate_bpmn_from_sql

def main():
    """Generate BPMN diagrams from task_definitions.sql"""
    
    print("🔄 Generating BPMN Diagram from task_definitions.sql")
    print("=" * 60)
    
    # Path to your SQL file
    sql_file_path = "database/sql/task_definitions.sql"
    
    if not os.path.exists(sql_file_path):
        print(f"❌ SQL file not found: {sql_file_path}")
        return
    
    try:
        # Generate BPMN artifacts
        result = generate_bpmn_from_sql(sql_file_path=sql_file_path)
        
        # Create output directory
        output_dir = "docs/workflow_diagrams"
        os.makedirs(output_dir, exist_ok=True)
        
        # Write BPMN XML file
        bpmn_file = os.path.join(output_dir, "application_certification_workflow.bpmn")
        with open(bpmn_file, 'w', encoding='utf-8') as f:
            f.write(result['bpmn_xml'])
        
        # Write Mermaid diagram
        mermaid_file = os.path.join(output_dir, "application_certification_workflow.mmd")
        with open(mermaid_file, 'w', encoding='utf-8') as f:
            f.write(result['mermaid'])
        
        # Write analysis report
        analysis_file = os.path.join(output_dir, "workflow_analysis.md")
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(result['summary'])
        
        # Write HTML viewer for Mermaid
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Application Certification Workflow</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .diagram {{ text-align: center; margin: 20px 0; }}
        .info {{ background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>🏢 Application Certification Workflow</h1>
    
    <div class="info">
        <h3>📊 Workflow Statistics:</h3>
        <ul>
            <li><strong>Total Tasks:</strong> {result['stats']['total_tasks']}</li>
            <li><strong>Total Flows:</strong> {result['stats']['total_flows']}</li>
            <li><strong>Lanes (Swimlanes):</strong> {result['stats']['total_lanes']}</li>
            <li><strong>Task Types:</strong> {', '.join(result['stats']['task_types'])}</li>
            <li><strong>Roles:</strong> {', '.join(result['stats']['roles'])}</li>
        </ul>
    </div>
    
    <div class="diagram">
        <div class="mermaid">
{result['mermaid']}
        </div>
    </div>
    
    <div class="info">
        <h3>🔗 Related Files:</h3>
        <ul>
            <li><a href="application_certification_workflow.bpmn">BPMN 2.0 XML</a> - For BPMN tools (Camunda, etc.)</li>
            <li><a href="application_certification_workflow.mmd">Mermaid Source</a> - Raw Mermaid syntax</li>
            <li><a href="workflow_analysis.md">Detailed Analysis</a> - Complete workflow breakdown</li>
        </ul>
    </div>
    
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>"""
        
        html_file = os.path.join(output_dir, "workflow_viewer.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Print summary
        print("✅ BPMN Generation Complete!")
        print(f"\n📁 Generated files in {output_dir}:")
        print(f"   📄 application_certification_workflow.bpmn - BPMN 2.0 XML")
        print(f"   🔀 application_certification_workflow.mmd  - Mermaid diagram")
        print(f"   📊 workflow_analysis.md                     - Analysis report")
        print(f"   🌐 workflow_viewer.html                     - Interactive viewer")
        
        print(f"\n📊 Workflow Statistics:")
        print(f"   🎯 Total Tasks: {result['stats']['total_tasks']}")
        print(f"   ➡️  Total Flows: {result['stats']['total_flows']}")
        print(f"   🏊 Swimlanes: {result['stats']['total_lanes']}")
        print(f"   🔧 Task Types: {', '.join(result['stats']['task_types'])}")
        print(f"   👥 Roles: {', '.join(result['stats']['roles'])}")
        
        print(f"\n🌐 To view the interactive diagram:")
        print(f"   Open: {os.path.abspath(html_file)}")
        
        print(f"\n💡 Usage Tips:")
        print(f"   • Import .bpmn file into Camunda Modeler, BPMN.io, or similar tools")
        print(f"   • Use .mmd file with Mermaid Live Editor (mermaid.live)")
        print(f"   • View .html file in any web browser for interactive diagram")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating BPMN: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)