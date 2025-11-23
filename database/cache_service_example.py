"""
Example usage of DatabaseCacheService

This file demonstrates how to use the static cache service
for TaskDefinition and TaskFlow tables.
"""

from database.cache_service import get_cache, DatabaseCacheService


def example_basic_usage():
    """Basic usage examples"""
    
    # Get the singleton instance (two ways)
    cache1 = get_cache()
    cache2 = DatabaseCacheService.get_instance()
    
    # Both references point to the same singleton
    assert cache1 is cache2
    
    # Cache loads automatically on first access (lazy loading)
    # Or you can force load
    cache1.load()
    
    # Get cache statistics
    stats = cache1.get_stats()
    print(f"Cache stats: {stats}")


def example_task_definition_access():
    """Examples of accessing TaskDefinition data"""
    
    cache = get_cache()
    
    # Get single task definition by ID
    task_def = cache.get_task_definition(task_id=123)
    
    if task_def:
        # Access using getattr() - as requested
        task_name = getattr(task_def, 'TaskName')
        task_type = getattr(task_def, 'TaskType')
        sequence = getattr(task_def, 'Sequence')
        
        # Also works with direct attribute access
        task_name = task_def.TaskName
        task_type = task_def.TaskType
        
        # Dictionary-style access also works
        task_name = task_def['TaskName']
        
        # Safe access with default
        custom_field = task_def.get('CustomField', 'default_value')
        
        # Get the underlying dictionary
        task_dict = task_def.to_dict()
        
        print(f"Task: {task_name}, Type: {task_type}, Sequence: {sequence}")
    
    # Get all task definitions
    all_tasks = cache.get_all_task_definitions()
    for task_id, task_def in all_tasks.items():
        print(f"TaskId: {task_id}, Name: {task_def.TaskName}")
    
    # Get tasks by stage
    stage_tasks = cache.get_task_definitions_by_stage(stage_id=5)
    for task_def in stage_tasks:
        print(f"Stage task: {task_def.TaskName}")
    
    # Get tasks by type
    start_tasks = cache.get_task_definitions_by_type(task_type='START')
    for task_def in start_tasks:
        print(f"Start task: {task_def.TaskName}")


def example_task_flow_access():
    """Examples of accessing TaskFlow data"""
    
    cache = get_cache()
    
    # Get single task flow by ID
    flow = cache.get_task_flow(flow_id=1)
    
    if flow:
        # Access using getattr()
        from_task_id = getattr(flow, 'FromTaskId')
        to_task_id = getattr(flow, 'ToTaskId')
        condition = getattr(flow, 'Condition')
        is_default = getattr(flow, 'IsDefault')
        
        print(f"Flow: {from_task_id} -> {to_task_id}, Condition: {condition}")
    
    # Get all outgoing flows from a task
    outgoing_flows = cache.get_task_flows_from(from_task_id=123)
    for flow in outgoing_flows:
        to_task_id = getattr(flow, 'ToTaskId')
        print(f"Outgoing flow to task: {to_task_id}")
    
    # Get all incoming flows to a task
    incoming_flows = cache.get_task_flows_to(to_task_id=456)
    for flow in incoming_flows:
        from_task_id = getattr(flow, 'FromTaskId')
        print(f"Incoming flow from task: {from_task_id}")
    
    # Get all task flows
    all_flows = cache.get_all_task_flows()
    for flow_id, flow in all_flows.items():
        print(f"FlowId: {flow_id}, {flow.FromTaskId} -> {flow.ToTaskId}")


def example_workflow_navigation():
    """Example: Navigate a workflow using the cache"""
    
    cache = get_cache()
    
    # Start with a START task
    start_tasks = cache.get_task_definitions_by_type('START')
    
    if start_tasks:
        start_task = start_tasks[0]
        task_id = getattr(start_task, 'TaskId')
        
        print(f"Starting workflow from: {start_task.TaskName}")
        
        # Get next tasks in the workflow
        outgoing_flows = cache.get_task_flows_from(from_task_id=task_id)
        
        for flow in outgoing_flows:
            next_task_id = getattr(flow, 'ToTaskId')
            next_task = cache.get_task_definition(next_task_id)
            
            if next_task:
                condition = getattr(flow, 'Condition', None)
                print(f"  Next task: {next_task.TaskName}")
                if condition:
                    print(f"    Condition: {condition}")


def example_cache_management():
    """Examples of cache management operations"""
    
    cache = get_cache()
    
    # Check if cache is loaded
    if cache.is_loaded():
        print("Cache is loaded")
    
    # Get statistics
    stats = cache.get_stats()
    print(f"Task Definitions: {stats['task_definitions_count']}")
    print(f"Task Flows: {stats['task_flows_count']}")
    
    # Reload cache (if data has changed)
    cache.reload()
    
    # Clear cache (if needed)
    cache.clear()
    
    # Cache will auto-load on next access
    task_def = cache.get_task_definition(1)


def example_integration_with_existing_code():
    """Example: Using cache in existing workflow code"""
    
    cache = get_cache()
    
    def process_task_instance(task_instance_id: int, task_id: int):
        """Process a task instance using cached task definition"""
        
        # Instead of querying database:
        # task_def = TaskDefinition.query.filter_by(TaskId=task_id).first()
        
        # Use cache:
        task_def = cache.get_task_definition(task_id)
        
        if not task_def:
            raise Exception(f"Task definition not found: {task_id}")
        
        # Access fields using getattr as before
        task_name = getattr(task_def, 'TaskName')
        task_type = getattr(task_def, 'TaskType')
        auto_complete = getattr(task_def, 'AutoComplete')
        
        print(f"Processing: {task_name} (Type: {task_type})")
        
        # Get next tasks
        if task_type != 'END':
            outgoing_flows = cache.get_task_flows_from(from_task_id=task_id)
            
            for flow in outgoing_flows:
                next_task_id = getattr(flow, 'ToTaskId')
                next_task_def = cache.get_task_definition(next_task_id)
                
                if next_task_def:
                    print(f"  Next: {next_task_def.TaskName}")


if __name__ == '__main__':
    # Run examples
    print("=== Basic Usage ===")
    example_basic_usage()
    
    print("\n=== Task Definition Access ===")
    example_task_definition_access()
    
    print("\n=== Task Flow Access ===")
    example_task_flow_access()
    
    print("\n=== Workflow Navigation ===")
    example_workflow_navigation()
    
    print("\n=== Cache Management ===")
    example_cache_management()
