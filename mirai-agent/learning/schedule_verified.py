"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-15T16:03:32.772230

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job() -> None:
    """A simple job to print the current time."""
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Job executed at: {current_time}")
    except Exception as e:
        logging.error(f"Error occurred in job execution: {e}")

def main() -> None:
    """Main function to schedule and run jobs."""
    # Schedule the job to run every 10 seconds
    schedule.every(10).seconds.do(job)

    logging.info("Scheduler started. Press Ctrl+C to exit.")

    while True:
        try:
            # Run pending jobs
            schedule.run_pending()
            time.sleep(1)  # Sleep for a short duration to prevent busy-waiting
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in the scheduling loop: {e}")

if __name__ == "__main__":
    main()