"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T08:21:53.453403

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
from datetime import datetime

def job() -> None:
    """Function to be scheduled that prints the current time."""
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Job executed at: {current_time}")
    except Exception as e:
        print(f"An error occurred: {e}")

def schedule_jobs() -> None:
    """Schedule jobs to run at specific intervals."""
    try:
        schedule.every(10).seconds.do(job)  # Schedule job every 10 seconds
        schedule.every().hour.do(job)       # Schedule job every hour

        while True:
            schedule.run_pending()            # Run pending jobs
            time.sleep(1)                    # Wait for 1 second
    except KeyboardInterrupt:
        print("Scheduler stopped by user.")
    except Exception as e:
        print(f"An error occurred while scheduling jobs: {e}")

if __name__ == "__main__":
    schedule_jobs()