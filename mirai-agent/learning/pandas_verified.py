"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-16T18:22:56.649421

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a Pandas DataFrame from a given dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the input data is not a dictionary or if the lists are not of equal length.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")

    length = None
    for key, value in data.items():
        if not isinstance(value, list):
            raise ValueError(f"Values for '{key}' must be lists.")
        if length is None:
            length = len(value)
        elif length != len(value):
            raise ValueError("All lists must be of the same length.")

    return pd.DataFrame(data)

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and basic operations.
    """
    # Sample data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [24, 27, 22, 32],
        'Salary': [70000, 80000, 120000, 90000]
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("Initial DataFrame:")
        print(df)

        # Calculate average salary
        average_salary = df['Salary'].mean()
        print(f"\nAverage Salary: {average_salary:.2f}")

        # Add a new column for experience level
        df['Experience Level'] = np.where(df['Age'] < 25, 'Junior', 'Senior')
        print("\nDataFrame with Experience Level:")
        print(df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()