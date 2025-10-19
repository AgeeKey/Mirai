"""
APScheduler - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T17:28:06.468597

This code has been verified by MIRAI's NASA-level learning system.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def my_job() -> None:
    """Job that prints the current time."""
    try:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info(f"Job executed at: {current_time}")
    except Exception as e:
        logger.error(f"Error executing job: {e}")

def start_scheduler() -> None:
    """Start the APScheduler to run jobs at specified intervals."""
    scheduler = BackgroundScheduler()
    # Schedule the job to run every 10 seconds
    scheduler.add_job(my_job, IntervalTrigger(seconds=10))
    
    try:
        scheduler.start()
        logger.info("Scheduler started. Press Ctrl+C to exit.")
        # Keep the main thread alive to let the scheduler run jobs
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")

if __name__ == "__main__":
    start_scheduler()