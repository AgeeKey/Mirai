"""
datetime - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 1/1
Learned: 2025-10-13T17:24:07.657968

This code has been verified by MIRAI's NASA-level learning system.
"""

from datetime import datetime, timedelta
from typing import Optional

def calculate_date_difference(start_date: str, end_date: str) -> Optional[int]:
    """
    Calculate the difference in days between two dates.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        Optional[int]: The difference in days, or None if input is invalid.
    """
    try:
        # Parse the input dates
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Calculate the difference in days
        difference = (end - start).days
        
        return difference
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return None

def main() -> None:
    """
    Main function to demonstrate the date difference calculation.
    """
    start_date = '2023-01-01'
    end_date = '2023-10-31'
    
    # Calculate the difference in days
    days_difference = calculate_date_difference(start_date, end_date)
    
    if days_difference is not None:
        print(f"The difference between {start_date} and {end_date} is {days_difference} days.")
    else:
        print("Could not calculate the date difference due to invalid input.")

if __name__ == "__main__":
    main()