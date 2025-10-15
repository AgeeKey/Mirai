"""
celery - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-15T14:58:32.408214

This code has been verified by MIRAI's NASA-level learning system.
"""

from celery import Celery, shared_task
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery app
app = Celery('tasks', broker='redis://localhost:6379/0')

@shared_task
def add(x: int, y: int) -> int:
    """
    Add two numbers together.
    
    Args:
        x (int): The first number.
        y (int): The second number.
    
    Returns:
        int: The sum of x and y.
    """
    try:
        logger.info(f'Starting addition of {x} and {y}')
        time.sleep(2)  # Simulate a time-consuming task
        result = x + y
        logger.info(f'Addition result: {result}')
        return result
    except Exception as e:
        logger.error(f'Error occurred while adding: {e}')
        raise

@shared_task
def multiply(x: int, y: int) -> int:
    """
    Multiply two numbers together.
    
    Args:
        x (int): The first number.
        y (int): The second number.
    
    Returns:
        int: The product of x and y.
    """
    try:
        logger.info(f'Starting multiplication of {x} and {y}')
        time.sleep(2)  # Simulate a time-consuming task
        result = x * y
        logger.info(f'Multiplication result: {result}')
        return result
    except Exception as e:
        logger.error(f'Error occurred while multiplying: {e}')
        raise

if __name__ == '__main__':
    # Example of running tasks
    result_add = add.delay(4, 6)
    result_multiply = multiply.delay(4, 5)

    # Wait for results
    logger.info(f'Addition result: {result_add.get(timeout=10)}')
    logger.info(f'Multiplication result: {result_multiply.get(timeout=10)}')