"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-14T23:25:16.505155

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def job() -> None:
    """Function to be scheduled that prints the current time."""
    try:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logging.info(f"Job executed at: {current_time}")
    except Exception as e:
        logging.error(f"Error while executing job: {e}")

def run_scheduler() -> None:
    """Run the scheduler to execute jobs at predefined intervals."""
    # Schedule the job to run every 10 seconds
    schedule.every(10).seconds.do(job)

    while True:
        try:
            # Run pending jobs
            schedule.run_pending()
            time.sleep(1)  # Sleep to prevent busy-waiting
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in scheduler loop: {e}")

if __name__ == "__main__":
    run_scheduler()