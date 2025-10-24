"""
Background Task Integration for API Logic Server
Integrate the background scheduler with the Flask application
"""

import logging
import flask
from integration.background.background_scheduler import BackgroundScheduler

logger = logging.getLogger(__name__)

# Global Flask app reference for background tasks
_flask_app = None

def get_flask_app():
    """Get the Flask app instance for background tasks"""
    return _flask_app

def initialize_background_scheduler(app):
    """
    Initialize and start the background scheduler
    Call this from your Flask app startup
    """
    global _flask_app,_task_manager
    _flask_app = app  # Store Flask app reference for background tasks
    
    try:
        _task_manager = BackgroundScheduler(app)
        # Add scheduler management endpoints
        _task_manager.add_background_endpoints(app)
        
        # Setup background jobs based on environment
        if app.config.get('ENV') == 'production':
            #setup_production_jobs()
            logger.info("🏭 Production background jobs configured")
        else:
            _task_manager.setup_jobs()
            logger.info("🧪 Development background jobs configured")
        
        # Setup enhanced background task manager
        _task_manager.start()
        
        logger.info("✅ Background scheduler initialized successfully")
        logger.info(f"🔗 Flask app stored for background tasks: {_flask_app is not None}")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize background scheduler: {e}")
        raise

def shutdown_background_scheduler():
    """
    Gracefully shutdown the background scheduler
    Call this during app shutdown
    """
    try:
        _task_manager.stop()
        logger.info("🛑 Background scheduler shutdown complete")
    except Exception as e:
        logger.error(f"Error during scheduler shutdown: {e}")

# Example custom tasks specific to your application
def check_cognito_token_health():
    """Check AWS Cognito token health every minute"""
    try:
        logger.info("🔍 Checking Cognito token health")
        
        # Add your Cognito health check logic here
        # For example:
        # - Check token expiration times
        # - Validate JWKS endpoint accessibility
        # - Monitor authentication success rates
        
    except Exception as e:
        logger.error(f"Cognito health check failed: {e}")

def sync_sharepoint_documents():
    """Sync SharePoint documents every 5 minutes"""
    try:
        logger.info("📄 Syncing SharePoint documents")
        
        # Add your SharePoint sync logic here
        # For example:
        # - Check for new documents
        # - Update document metadata
        # - Process document workflows
        
    except Exception as e:
        logger.error(f"SharePoint sync failed: {e}")

def cleanup_session_data():
    """Clean up expired session data"""
    try:
        logger.info("🧹 Cleaning up expired sessions")
        
        # Add your session cleanup logic here
        # For example:
        # - Remove expired Flask sessions
        # - Clean up temporary files
        # - Archive old workflow data
        
    except Exception as e:
        logger.error(f"Session cleanup failed: {e}")

def setup_custom_jobs():
    """Setup custom background jobs for your application"""
    
    # Check Cognito health every minute
    _task_manager.add_job_every_minute(
        check_cognito_token_health,
        job_name="cognito_health_check"
    )
    
    # Sync SharePoint every 5 minutes
    _task_manager.add_job_every_n_minutes(
        sync_sharepoint_documents,
        minutes=5,
        job_name="sharepoint_sync"
    )
    
    # Clean up sessions every 30 minutes
    _task_manager.add_job_every_n_minutes(
        cleanup_session_data,
        minutes=30,
        job_name="session_cleanup"
    )
    
    logger.info("🔧 Custom background jobs configured")