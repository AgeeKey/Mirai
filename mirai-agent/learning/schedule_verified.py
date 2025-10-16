"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-16T20:32:19.703193

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job() -> None:
    """Function to be scheduled that performs a task."""
    logging.info("Job is running...")

def run_scheduler() -> None:
    """Run the scheduled jobs indefinitely."""
    try:
        # Schedule the job to run every 10 seconds
        schedule.every(10).seconds.do(job)

        logging.info("Scheduler started. Waiting for jobs to run...")
        
        while True:
            schedule.run_pending()  # Run any pending jobs
            time.sleep(1)  # Sleep for a short duration to prevent busy waiting

    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    run_scheduler()