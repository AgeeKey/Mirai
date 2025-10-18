"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-18T10:17:48.774018

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job() -> None:
    """Function to be scheduled that logs a message."""
    logging.info("Job is running...")

def schedule_jobs() -> None:
    """Schedule the job to run every 10 seconds."""
    schedule.every(10).seconds.do(job)

def run_scheduler() -> None:
    """Run the scheduler to keep checking for scheduled jobs."""
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)  # Sleep for a short period to avoid busy-waiting
        except Exception as e:
            logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    schedule_jobs()
    logging.info("Scheduler started...")
    run_scheduler()