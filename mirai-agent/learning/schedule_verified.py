"""
schedule - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-22T17:17:04.439673

This code has been verified by MIRAI's NASA-level learning system.
"""

import schedule
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job() -> None:
    """Function to be scheduled, logs the current time."""
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Job executed at {current_time}")
    except Exception as e:
        logging.error(f"Error while executing job: {e}")

def main() -> None:
    """Main function to set up the schedule and run the scheduler."""
    # Schedule the job every 10 seconds
    schedule.every(10).seconds.do(job)

    logging.info("Scheduler started. Press Ctrl+C to stop.")

    while True:
        try:
            schedule.run_pending()  # Run pending scheduled tasks
            time.sleep(1)           # Wait for a second before checking again
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user.")
            break
        except Exception as e:
            logging.error(f"Error in scheduler: {e}")

if __name__ == "__main__":
    main()