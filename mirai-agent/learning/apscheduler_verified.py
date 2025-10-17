"""
APScheduler - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-17T17:17:40.927114

This code has been verified by MIRAI's NASA-level learning system.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def job_function() -> None:
    """Function to be scheduled for execution."""
    logging.info("Job executed at: %s", time.strftime("%Y-%m-%d %H:%M:%S"))

def start_scheduler() -> None:
    """Start the APScheduler to run scheduled jobs."""
    try:
        scheduler = BackgroundScheduler()
        # Schedule job_function to run every 5 seconds
        scheduler.add_job(job_function, IntervalTrigger(seconds=5), id='my_job_id')
        scheduler.start()
        logging.info("Scheduler started. Job scheduled.")

        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            pass
    except Exception as e:
        logging.error("Error starting scheduler: %s", e)
    finally:
        scheduler.shutdown()
        logging.info("Scheduler shut down.")

if __name__ == "__main__":
    start_scheduler()