"""
Database Cache Service - Singleton Pattern
Provides in-memory caching for TaskDefinition, StageDefinition, and TaskFlow tables
with dictionary-like attribute access using getattr()
"""
import logging
from typing import Dict, List, Optional, Any
from threading import Lock
from database.models import TaskDefinition, StageDefinition, TaskFlow
from safrs import DB

app_logger = logging.getLogger("api_logic_server_app")


class CachedObject:
    """Wrapper class to provide attribute-style access to cached data"""
    
    def __init__(self, data_dict: Dict[str, Any]):
        self._data = data_dict
    
    def __getattr__(self, name: str) -> Any:
        """Allow attribute-style access: obj.field_name"""
        if name.startswith('_'):
            # Allow access to private attributes like _data
            return object.__getattribute__(self, name)
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access: obj['field_name']"""
        return self._data[key]
    
    def get(self, key: str, default=None) -> Any:
        """Safe dictionary-style access with default"""
        return self._data.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the underlying dictionary"""
        return self._data.copy()
    
    def __repr__(self) -> str:
        return f"CachedObject({self._data})"


class DatabaseCacheService:
    """
    Singleton cache service for TaskDefinition, StageDefinition, and TaskFlow tables.
    
    Usage:
        # Get the singleton instance
        cache = DatabaseCacheService.get_instance()
        
        # Access task definition by ID
        task_def = cache.get_task_definition(task_id=123)
        task_name = getattr(task_def, 'TaskName')
        
        # Access stage definition by ID
        stage_def = cache.get_stage_definition(stage_id=5)
        stage_name = getattr(stage_def, 'StageName')
        
        # Access all task definitions
        all_tasks = cache.get_all_task_definitions()
        
        # Access task flows
        flows = cache.get_task_flows_from(from_task_id=123)
        flows = cache.get_task_flows_to(to_task_id=456)
        
        # Reload cache if needed
        cache.reload()
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseCacheService, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._task_definitions: Dict[int, CachedObject] = {}
        self._stage_definitions: Dict[int, CachedObject] = {}
        self._task_flows: Dict[int, CachedObject] = {}
        self._task_flows_by_from_task: Dict[int, List[CachedObject]] = {}
        self._task_flows_by_to_task: Dict[int, List[CachedObject]] = {}
        self._loaded = False
        
        app_logger.info("📦 DatabaseCacheService singleton instance created")
    
    @classmethod
    def get_instance(cls) -> 'DatabaseCacheService':
        """Get the singleton instance of the cache service"""
        return cls()
    
    def _load_task_definitions(self):
        """Load all TaskDefinition records into cache"""
        try:
            session = DB.session
            task_defs = session.query(TaskDefinition).all()
            
            self._task_definitions.clear()
            
            for task_def in task_defs:
                # Convert SQLAlchemy model to dictionary
                task_dict = {
                    'TaskId': task_def.TaskId,
                    'ProcessDefinitionId': task_def.ProcessDefinitionId,
                    'TaskName': task_def.TaskName,
                    'TaskType': task_def.TaskType,
                    'TaskCategory': task_def.TaskCategory,
                    'Sequence': task_def.Sequence,
                    'StageDefinitionId': task_def.StageDefinitionId,
                    'IsParallel': task_def.IsParallel,
                    'AssigneeRole': task_def.AssigneeRole,
                    'EstimatedDurationMinutes': task_def.EstimatedDurationMinutes,
                    'IsRequired': task_def.IsRequired,
                    'AutoComplete': task_def.AutoComplete,
                    'Description': task_def.Description,
                    'CreatedDate': task_def.CreatedDate,
                    'CreatedBy': task_def.CreatedBy,
                    'ModifiedDate': task_def.ModifiedDate,
                    'ModifiedBy': task_def.ModifiedBy,
                    'PreScriptJson': task_def.PreScriptJson,
                    'PostScriptJson': task_def.PostScriptJson
                }
                
                self._task_definitions[task_def.TaskId] = CachedObject(task_dict)
            
            app_logger.info(f"✅ Loaded {len(self._task_definitions)} TaskDefinition records into cache")
            
        except Exception as e:
            app_logger.error(f"❌ Error loading TaskDefinition cache: {str(e)}")
            raise
    
    def _load_stage_definitions(self):
        """Load all StageDefinition records into cache"""
        try:
            session = DB.session
            stage_defs = session.query(StageDefinition).all()
            
            self._stage_definitions.clear()
        
            for stage_def in stage_defs:
                # Convert SQLAlchemy model to dictionary
                stage_dict = {
                    'StageId': stage_def.StageId,
                    'StageName': stage_def.StageName,
                    'StageDescription': stage_def.StageDescription,
                    'EstimatedDurationDays': stage_def.EstimatedDurationDays,
                    'CreatedDate': stage_def.CreatedDate,
                    'CreatedBy': stage_def.CreatedBy,
                    'ModifiedDate': stage_def.ModifiedDate,
                    'ModifiedBy': stage_def.ModifiedBy
                }
                
                cached_stage = CachedObject(stage_dict)
                self._stage_definitions[stage_def.StageId] = cached_stage
                
                
            app_logger.info(f"✅ Loaded {len(self._stage_definitions)} StageDefinition records into cache")
            
        except Exception as e:
            app_logger.error(f"❌ Error loading StageDefinition cache: {str(e)}")
            raise
    
    def _load_task_flows(self):
        """Load all TaskFlow records into cache with indexed lookups"""
        try:
            session = DB.session
            task_flows = session.query(TaskFlow).all()
            
            self._task_flows.clear()
            self._task_flows_by_from_task.clear()
            self._task_flows_by_to_task.clear()
            
            for flow in task_flows:
                # Convert SQLAlchemy model to dictionary
                flow_dict = {
                    'FlowId': flow.FlowId,
                    'FromTaskId': flow.FromTaskId,
                    'ToTaskId': flow.ToTaskId,
                    'Condition': flow.Condition,
                    'IsDefault': flow.IsDefault
                }
                
                cached_flow = CachedObject(flow_dict)
                self._task_flows[flow.FlowId] = cached_flow
                
                # Index by FromTaskId
                if flow.FromTaskId is not None:
                    if flow.FromTaskId not in self._task_flows_by_from_task:
                        self._task_flows_by_from_task[flow.FromTaskId] = []
                    self._task_flows_by_from_task[flow.FromTaskId].append(cached_flow)
                
                # Index by ToTaskId
                if flow.ToTaskId is not None:
                    if flow.ToTaskId not in self._task_flows_by_to_task:
                        self._task_flows_by_to_task[flow.ToTaskId] = []
                    self._task_flows_by_to_task[flow.ToTaskId].append(cached_flow)
            
            app_logger.info(f"✅ Loaded {len(self._task_flows)} TaskFlow records into cache")
            app_logger.info(f"   📊 Indexed {len(self._task_flows_by_from_task)} FromTask lookups")
            app_logger.info(f"   📊 Indexed {len(self._task_flows_by_to_task)} ToTask lookups")
            
        except Exception as e:
            app_logger.error(f"❌ Error loading TaskFlow cache: {str(e)}")
            raise
    
    def load(self, flask_app=None):
        """Load all data into cache (thread-safe)
        
        Args:
            flask_app: Optional Flask app instance for app context
        """
        with self._lock:
            if self._loaded:
                app_logger.debug("Cache already loaded, skipping")
                return
            
            app_logger.info("🔄 Loading database cache...")
            
            # Use Flask app context if provided
            if flask_app:
                with flask_app.app_context():
                    self._load_task_definitions()
                    self._load_stage_definitions()
                    self._load_task_flows()
            else:
                self._load_task_definitions()
                self._load_stage_definitions()
                self._load_task_flows()
            
            self._loaded = True
            app_logger.info("✅ Database cache loaded successfully")
    
    def reload(self, flask_app=None):
        """Force reload of all cache data
        
        Args:
            flask_app: Optional Flask app instance for app context
        """
        with self._lock:
            app_logger.info("🔄 Reloading database cache...")
            self._loaded = False
            self.load(flask_app)
    
    def ensure_loaded(self):
        """Ensure cache is loaded (lazy loading)"""
        if not self._loaded:
            self.load()
    
    # ============================================
    # TaskDefinition Access Methods
    # ============================================
    
    def get_task_definition(self, task_id: int) -> Optional[CachedObject]:
        """
        Get a TaskDefinition by TaskId
        
        Args:
            task_id: The TaskId to lookup
            
        Returns:
            CachedObject with TaskDefinition data or None if not found
            
        Usage:
            task_def = cache.get_task_definition(123)
            if task_def:
                name = getattr(task_def, 'TaskName')
                task_type = task_def.TaskType  # Also works
        """
        self.ensure_loaded()
        return self._task_definitions.get(task_id)
    
    def get_all_task_definitions(self) -> Dict[int, CachedObject]:
        """
        Get all TaskDefinitions
        
        Returns:
            Dictionary mapping TaskId to CachedObject
        """
        self.ensure_loaded()
        return self._task_definitions.copy()
    
    def get_task_definitions_by_stage(self, stage_id: int) -> List[CachedObject]:
        """
        Get all TaskDefinitions for a specific StageDefinitionId
        
        Args:
            stage_id: The StageDefinitionId to filter by
            
        Returns:
            List of CachedObject instances
        """
        self.ensure_loaded()
        return [
            task_def for task_def in self._task_definitions.values()
            if task_def.StageDefinitionId == stage_id
        ]
    
    def get_task_definitions_by_type(self, task_type: str) -> List[CachedObject]:
        """
        Get all TaskDefinitions of a specific type
        
        Args:
            task_type: The TaskType to filter by (e.g., 'START', 'END', 'GATEWAY')
            
        Returns:
            List of CachedObject instances
        """
        self.ensure_loaded()
        return [
            task_def for task_def in self._task_definitions.values()
            if task_def.TaskType == task_type
        ]
    
    # ============================================
    # StageDefinition Access Methods
    # ============================================
    
    def get_stage_definition(self, stage_id: int) -> Optional[CachedObject]:
        """
        Get a StageDefinition by StageId
        
        Args:
            stage_id: The StageId to lookup
            
        Returns:
            CachedObject with StageDefinition data or None if not found
            
        Usage:
            stage_def = cache.get_stage_definition(5)
            if stage_def:
                name = getattr(stage_def, 'StageName')
                description = stage_def.StageDescription  # Also works
        """
        self.ensure_loaded()
        return self._stage_definitions.get(stage_id)
    
    def get_all_stage_definitions(self) -> Dict[int, CachedObject]:
        """
        Get all StageDefinitions
        
        Returns:
            Dictionary mapping StageId to CachedObject
        """
        self.ensure_loaded()
        return self._stage_definitions.copy()
    
    # ============================================
    # TaskFlow Access Methods
    # ============================================
    
    def get_task_flow(self, flow_id: int) -> Optional[CachedObject]:
        """
        Get a TaskFlow by FlowId
        
        Args:
            flow_id: The FlowId to lookup
            
        Returns:
            CachedObject with TaskFlow data or None if not found
        """
        self.ensure_loaded()
        return self._task_flows.get(flow_id)
    
    def get_all_task_flows(self) -> Dict[int, CachedObject]:
        """
        Get all TaskFlows
        
        Returns:
            Dictionary mapping FlowId to CachedObject
        """
        self.ensure_loaded()
        return self._task_flows.copy()
    
    def get_task_flows_from(self, from_task_id: int) -> List[CachedObject]:
        """
        Get all TaskFlows originating FROM a specific task
        
        Args:
            from_task_id: The FromTaskId to filter by
            
        Returns:
            List of CachedObject instances (outgoing flows)
            
        Usage:
            outgoing_flows = cache.get_task_flows_from(123)
            for flow in outgoing_flows:
                to_task_id = getattr(flow, 'ToTaskId')
        """
        self.ensure_loaded()
        return self._task_flows_by_from_task.get(from_task_id, []).copy()
    
    def get_task_flows_to(self, to_task_id: int) -> List[CachedObject]:
        """
        Get all TaskFlows going TO a specific task
        
        Args:
            to_task_id: The ToTaskId to filter by
            
        Returns:
            List of CachedObject instances (incoming flows)
        """
        self.ensure_loaded()
        return self._task_flows_by_to_task.get(to_task_id, []).copy()
    
    # ============================================
    # Utility Methods
    # ============================================
    
    def is_loaded(self) -> bool:
        """Check if cache is loaded"""
        return self._loaded
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        self.ensure_loaded()
        return {
            'loaded': self._loaded,
            'task_definitions_count': len(self._task_definitions),
            'stage_definitions_count': len(self._stage_definitions),
            'task_flows_count': len(self._task_flows),
            'from_task_index_count': len(self._task_flows_by_from_task),
            'to_task_index_count': len(self._task_flows_by_to_task)
        }
    
    def clear(self):
        """Clear all cache data"""
        with self._lock:
            self._task_definitions.clear()
            self._stage_definitions.clear()
            self._task_flows.clear()
            self._task_flows_by_from_task.clear()
            self._task_flows_by_to_task.clear()
            self._loaded = False
            app_logger.info("🗑️ Database cache cleared")


# Convenience function for getting the singleton instance
def get_cache() -> DatabaseCacheService:
    """
    Get the singleton DatabaseCacheService instance
    
    Returns:
        DatabaseCacheService singleton instance
        
    Usage:
        from database.cache_service import get_cache
        
        cache = get_cache()
        task_def = cache.get_task_definition(123)
    """
    return DatabaseCacheService.get_instance()
