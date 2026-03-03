"""
Background Scheduler Service for API Logic Server
Provides periodic task execution capabilities
"""

import threading
import time
import schedule
import logging
from datetime import datetime
from typing import Callable, Dict, Any
import atexit
from flask import Flask

logger = logging.getLogger(__name__)
_flask_app = None
class BackgroundScheduler:
    """
    Background scheduler for running periodic tasks
    Supports minute, hourly, daily, and custom interval scheduling
    """

    def __init__(self, flask_app: Flask):
        self.flask_app = flask_app
        self.scheduler_thread = None
        self.is_running = False
        self.jobs = []
        self._stop_event = threading.Event()
        global _flask_app
        _flask_app = flask_app  # Store Flask app reference
        # Register cleanup on exit
        atexit.register(self.stop)
        return
    
    def start(self):
        """Start the background scheduler thread"""
        if self.is_running:
            logger.warning("Background scheduler is already running")
            return
        
        self.is_running = True
        self._stop_event.clear()
        
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("✅ Background scheduler started")
    
    def stop(self):
        """Stop the background scheduler thread"""
        if not self.is_running:
            return
        
        self.is_running = False
        self._stop_event.set()
        
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        
        schedule.clear()
        logger.info("🛑 Background scheduler stopped")
    
    def _run_scheduler(self):
        """Internal scheduler loop"""
        logger.info("Background scheduler thread started")
        
        while self.is_running and not self._stop_event.is_set():
            try:
                schedule.run_pending()
                # Check every second for pending jobs
                self._stop_event.wait(1)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)  # Wait before retrying
    
    def add_job_every_minute(self, func: Callable, job_name: str = None, **kwargs) -> str:
        """Add a job that runs every minute"""
        return self.add_job(func, "minute", 1, job_name, **kwargs)
    
    def add_job_every_n_minutes(self, func: Callable, minutes: int, job_name: str = None, **kwargs) -> str:
        """Add a job that runs every N minutes"""
        return self.add_job(func, "minute", minutes, job_name, **kwargs)
    
    def add_job_hourly(self, func: Callable, job_name: str = None, **kwargs) -> str:
        """Add a job that runs every hour"""
        return self.add_job(func, "hour", 1, job_name, **kwargs)
    
    def add_job_daily(self, func: Callable, at_time: str = "00:00", job_name: str = None, **kwargs) -> str:
        """Add a job that runs daily at specified time"""
        return self.add_job(func, "day", 1, job_name, at_time=at_time, **kwargs)
    
    def add_job(self, func: Callable, interval_type: str, interval: int, 
                job_name: str = None, **kwargs) -> str:
        """
        Add a scheduled job
        
        Args:
            func: Function to execute
            interval_type: 'second', 'minute', 'hour', 'day'
            interval: Number of intervals
            job_name: Optional job name for identification
            **kwargs: Additional arguments for the function
        
        Returns:
            str: Job ID for tracking
        """
        if not job_name:
            job_name = f"{func.__name__}_{len(self.jobs)}"
        
        # Wrap function to handle errors and logging
        def wrapped_func():
            try:
                start_time = datetime.now()
                logger.info(f"🔄 Starting job: {job_name}")
                
                result = func(**kwargs)
                
                duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"✅ Job completed: {job_name} (took {duration:.2f}s)")
                
                return result
                
            except Exception as e:
                logger.error(f"❌ Job failed: {job_name} - {e}")
                raise
        
        # Schedule the job
        if interval_type == "second":
            job = schedule.every(interval).seconds.do(wrapped_func)
        elif interval_type == "minute":
            job = schedule.every(interval).minutes.do(wrapped_func)
        elif interval_type == "hour":
            job = schedule.every(interval).hours.do(wrapped_func)
        elif interval_type == "day":
            at_time = kwargs.get('at_time', '00:00')
            job = schedule.every(interval).days.at(at_time).do(wrapped_func)
        else:
            raise ValueError(f"Invalid interval_type: {interval_type}")
        
        # Store job info
        job_info = {
            'job': job,
            'name': job_name,
            'func': func,
            'interval_type': interval_type,
            'interval': interval,
            'created_at': datetime.now()
        }
        
        self.jobs.append(job_info)
        
        logger.info(f"📅 Scheduled job: {job_name} - every {interval} {interval_type}(s)")
        
        return job_name
    
    def remove_job(self, job_name: str) -> bool:
        """Remove a scheduled job by name"""
        for i, job_info in enumerate(self.jobs):
            if job_info['name'] == job_name:
                schedule.cancel_job(job_info['job'])
                self.jobs.pop(i)
                logger.info(f"🗑️ Removed job: {job_name}")
                return True
        
        logger.warning(f"Job not found: {job_name}")
        return False
    
    def list_jobs(self) -> list:
        """Get list of all scheduled jobs"""
        return [{
            'name': job_info['name'],
            'interval': f"{job_info['interval']} {job_info['interval_type']}(s)",
            'next_run': job_info['job'].next_run,
            'created_at': job_info['created_at']
        } for job_info in self.jobs]
    
    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status information"""
        return {
            'is_running': self.is_running,
            'total_jobs': len(self.jobs),
            'jobs': self.list_jobs(),
            'next_run': min([job['job'].next_run for job in self.jobs]) if self.jobs else None
        }

    def setup_jobs(self):
        """Setup example background jobs"""
        from api.api_discovery.event_action import resolve_paid_invoices

        # Create a wrapper function that calls resolve_paid_invoices with the Flask app
        def resolve_paid_invoices_wrapper():
            try:
                logger.info("🔄 Starting Find Paid Invoices job")
                resolve_paid_invoices(app=self.flask_app)
                logger.info("✅ Find Paid Invoices job completed")
            except Exception as e:
                logger.error(f"❌ Find Paid Invoices job failed: {e}")

        self.add_job_every_n_minutes(
            resolve_paid_invoices_wrapper,
            minutes=10,  # Run every 10 minutes
            job_name="Find Paid Invoices"
        )

        from api.api_discovery.create_application import submsisson_request_process

        def create_submission_application_wrapper():
            try:
                logger.info("🔄 Starting Create Submission Application job")
                submsisson_request_process(app=self.flask_app)
                logger.info("✅ Create Submission Application job completed")
            except Exception as e:
                logger.error(f"❌ Create Submission Application job failed: {e}")

        self.add_job_every_n_minutes(
            create_submission_application_wrapper, 
            minutes=5,     
            job_name="Create Submission Application"
        )

    def add_background_endpoints(self, app: Flask):
        """Add background scheduler management endpoints to Flask app"""
        
        @app.route('/scheduler/status')
        def scheduler_status():
            """Get scheduler status"""
            return self.get_status()
        
        @app.route('/scheduler/jobs')
        def scheduler_jobs():
            """List all scheduled jobs"""
            return {"jobs": self.list_jobs()}
        
        @app.route('/scheduler/start', methods=['POST'])
        def scheduler_start():
            """Start the background scheduler"""
            try:
                self.start()
                return {"success": True, "message": "Scheduler started"}
            except Exception as e:
                return {"success": False, "error": str(e)}, 500
        
        @app.route('/scheduler/stop', methods=['POST'])
        def scheduler_stop():
            """Stop the background scheduler"""
            try:
                self.stop()
                return {"success": True, "message": "Scheduler stopped"}
            except Exception as e:
                return {"success": False, "error": str(e)}, 500
    

    

# Global scheduler instance - will be initialized when Flask app is available
background_scheduler = None

def get_background_scheduler(flask_app=None):
    """Get or create the global background scheduler"""
    global background_scheduler, _flask_app
    
    if background_scheduler is None:
        if flask_app:
            _flask_app = flask_app
            background_scheduler = BackgroundScheduler(flask_app)
            logger.info("✅ Global background scheduler initialized")
        elif _flask_app:
            background_scheduler = BackgroundScheduler(_flask_app)
            logger.info("✅ Global background scheduler initialized with stored app")
        else:
            logger.error("❌ Cannot create background scheduler - no Flask app available")
            return None
    
    return background_scheduler
# Example background tasks
def example_minute_task():
    """Example task that runs every minute"""
    logger.info(f"🕐 Minute task executed at {datetime.now()}")
    
    # Example: Database cleanup
    # cleanup_expired_sessions()
    
    # Example: Status monitoring
    # check_system_health()
    
    # Example: Data synchronization
    # sync_external_data()

def example_hourly_task():
    """Example task that runs every hour"""
    logger.info(f"⏰ Hourly task executed at {datetime.now()}")
    
    # Example: Generate reports
    # generate_hourly_report()
    
    # Example: Archive old data
    # archive_old_records()

def example_daily_task():
    """Example task that runs daily"""
    logger.info(f"📅 Daily task executed at {datetime.now()}")
    
    # Example: Backup database
    # backup_database()
    
    # Example: Send daily reports
    # send_daily_summary()

def setup_production_jobs():
    """Setup production background jobs"""
    from api.api_discovery.event_action import resolve_paid_invoices
    
    logger.info("🏭 Setting up production background jobs")
    
    # This function should be called by the main background_scheduler
    # Not implemented here as it's a standalone function
    
    '''
    # Add a job that runs every minute
    background_scheduler.add_job_every_minute(
        example_minute_task,
        job_name="system_monitor"
    )
    
    # Add a job that runs every 5 minutes
    background_scheduler.add_job_every_n_minutes(
        example_minute_task,
        minutes=5,
        job_name="data_sync"
    )
    
    # Add a job that runs every hour
    background_scheduler.add_job_hourly(
        example_hourly_task,
        job_name="hourly_reports"
    )
    
    # Add a job that runs daily at 2 AM
    background_scheduler.add_job_daily(
        example_daily_task,
        at_time="02:00",
        job_name="daily_backup"
    )
    '''
    
    logger.info("📋 Example background jobs configured")


# Custom business logic tasks
def cleanup_expired_tokens():
    """Clean up expired authentication tokens"""
    try:
        from flask import current_app
        # Add your token cleanup logic here
        logger.info("🧹 Cleaning up expired tokens")
        
        # Example: Remove tokens older than 24 hours
        # with current_app.app_context():
        #     expired_tokens = Token.query.filter(Token.expires_at < datetime.now()).all()
        #     for token in expired_tokens:
        #         db.session.delete(token)
        #     db.session.commit()
        #     logger.info(f"Removed {len(expired_tokens)} expired tokens")
        
    except Exception as e:
        logger.error(f"Error cleaning up tokens: {e}")

def process_pending_notifications():
    """Process pending notifications"""
    try:
        logger.info("📨 Processing pending notifications")
        
        # Example: Send pending emails
        # pending_notifications = Notification.query.filter_by(status='pending').all()
        # for notification in pending_notifications:
        #     send_notification(notification)
        #     notification.status = 'sent'
        # db.session.commit()
        
    except Exception as e:
        logger.error(f"Error processing notifications: {e}")

def sync_external_systems():
    """Synchronize data with external systems"""
    try:
        logger.info("🔄 Synchronizing with external systems")
        
        # Example: Sync with ERP system
        # sync_with_erp()
        
        # Example: Update from API
        # fetch_external_updates()
        
    except Exception as e:
        logger.error(f"Error syncing external systems: {e}")

def generate_system_reports():
    """Generate system performance reports"""
    try:
        logger.info("📊 Generating system reports")
        
        # Example: Database performance metrics
        # collect_db_metrics()
        
        # Example: API usage statistics
        # generate_api_usage_report()
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}")

def setup_production_jobs():
    """Setup production background jobs"""
    '''
    # Every minute: Token cleanup
    background_scheduler.add_job_every_minute(
        cleanup_expired_tokens,
        job_name="token_cleanup"
    )
    
    # Every 5 minutes: Process notifications
    background_scheduler.add_job_every_n_minutes(
        process_pending_notifications,
        minutes=5,
        job_name="notification_processor"
    )
    
    # Every 15 minutes: Sync external systems
    background_scheduler.add_job_every_n_minutes(
        sync_external_systems,
        minutes=15,
        job_name="external_sync"
    )
    
    # Every hour: Generate reports
    background_scheduler.add_job_hourly(
        generate_system_reports,
        job_name="system_reports"
    )
    '''
    logger.info("🏭 Production background jobs configured")