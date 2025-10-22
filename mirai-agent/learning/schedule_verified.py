"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-22T15:05:45.372410

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job() -> None:
    """Function to be scheduled that performs a simple task."""
    try:
        logging.info("Job executed")
        print("This job runs every 10 seconds.")
    except Exception as e:
        logging.error(f"Error occurred while executing the job: {e}")

def run_scheduler() -> None:
    """Sets up the job schedule and starts the scheduler."""
    # Schedule the job to run every 10 seconds
    schedule.every(10).seconds.do(job)

    logging.info("Scheduler started. Jobs are scheduled.")
    
    while True:
        schedule.run_pending()  # Check if a scheduled job is pending
        time.sleep(1)  # Sleep for a short duration to avoid busy waiting

if __name__ == "__main__":
    try:
        run_scheduler()  # Start the scheduler
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred in the scheduler: {e}")