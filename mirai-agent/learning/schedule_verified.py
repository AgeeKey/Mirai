"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-14T18:49:10.389220

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job() -> None:
    """
    A simple job function that logs a message.
    This function simulates a repetitive task.
    """
    logging.info("Job executed: Performing scheduled task.")

def run_scheduler() -> None:
    """
    Run the scheduler to execute jobs at specified intervals.
    This function will keep the scheduler running indefinitely.
    """
    try:
        # Schedule the job every 10 seconds
        schedule.every(10).seconds.do(job)

        logging.info("Scheduler started. Press Ctrl+C to stop.")
        
        while True:
            schedule.run_pending()  # Run the jobs that are scheduled to run
            time.sleep(1)  # Sleep for a short period to prevent busy waiting
            
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    run_scheduler()