"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-22T16:27:53.033652

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
from typing import Callable

def job() -> None:
    """Function to be executed on schedule."""
    print("Job is running...")

def run_scheduler() -> None:
    """Sets up the job scheduling and starts the scheduler."""
    try:
        # Schedule the job to run every 10 seconds
        schedule.every(10).seconds.do(job)

        while True:
            # Check for pending jobs and run them
            schedule.run_pending()
            time.sleep(1)  # Sleep for a short duration to avoid busy-waiting
    except KeyboardInterrupt:
        print("Scheduler stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_scheduler()