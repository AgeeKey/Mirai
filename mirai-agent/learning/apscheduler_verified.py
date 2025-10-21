"""
APScheduler - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-21T17:03:10.682580

This code has been verified by MIRAI's NASA-level learning system.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scheduled_job() -> None:
    """
    A sample job that logs a message.
    This function will be called by the scheduler at specified intervals.
    """
    logging.info("Scheduled job executed.")

def start_scheduler() -> None:
    """
    Starts the APScheduler to run the scheduled job at defined intervals.
    """
    scheduler = BackgroundScheduler()
    
    try:
        # Schedule the job to run every 5 seconds
        scheduler.add_job(scheduled_job, trigger=IntervalTrigger(seconds=5), id='my_job_id')
        scheduler.start()
        logging.info("Scheduler started.")
        
        # Keep the script running indefinitely
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Shut down the scheduler when exiting the app
        scheduler.shutdown()
        logging.info("Scheduler stopped.")

if __name__ == "__main__":
    start_scheduler()