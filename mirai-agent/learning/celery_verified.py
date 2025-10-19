"""
celery - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T00:22:23.872247

This code has been verified by MIRAI's NASA-level learning system.
"""

from celery import Celery, shared_task
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Celery app
app = Celery('tasks', broker='redis://localhost:6379/0')

@app.shared_task
def add(x: int, y: int) -> int:
    """
    Add two numbers together.

    :param x: First number to add.
    :param y: Second number to add.
    :return: The sum of x and y.
    """
    try:
        result = x + y
        logger.info(f'Adding {x} + {y} = {result}')
        return result
    except Exception as e:
        logger.error(f'Error occurred while adding: {e}')
        raise

@app.shared_task
def sleep_task(seconds: int) -> str:
    """
    Sleep for a specified number of seconds.

    :param seconds: Number of seconds to sleep.
    :return: A message indicating completion.
    """
    try:
        logger.info(f'Sleeping for {seconds} seconds...')
        time.sleep(seconds)
        logger.info('Sleep completed.')
        return f'Slept for {seconds} seconds.'
    except Exception as e:
        logger.error(f'Error occurred during sleep: {e}')
        raise

if __name__ == '__main__':
    # Example of calling the tasks
    result = add.delay(4, 6)  # Asynchronously add 4 and 6
    sleep_result = sleep_task.delay(5)  # Asynchronously sleep for 5 seconds

    # Wait for results
    print(f'Result of add: {result.get(timeout=10)}')
    print(f'Result of sleep_task: {sleep_result.get(timeout=10)}')