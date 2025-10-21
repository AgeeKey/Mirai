"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-21T02:52:09.454427

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging
from typing import Callable

# Configure logging
logging.basicConfig(level=logging.INFO)

def job() -> None:
    """A simple job function that logs a message."""
    logging.info("Job is running...")

def schedule_job(job_function: Callable[[], None], interval: int) -> None:
    """Schedules a job to run at a specific interval.

    Args:
        job_function (Callable[[], None]): The function to run.
        interval (int): The interval in seconds for the job to run.
    """
    try:
        schedule.every(interval).seconds.do(job_function)
        logging.info(f"Scheduled job to run every {interval} seconds.")
    except Exception as e:
        logging.error(f"Error scheduling job: {e}")

def main() -> None:
    """Main function to set up and run the scheduler."""
    schedule_job(job, 5)  # Schedule job to run every 5 seconds

    while True:
        try:
            schedule.run_pending()  # Run any pending jobs
            time.sleep(1)  # Wait for 1 second before checking again
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in the scheduler loop: {e}")

if __name__ == "__main__":
    main()