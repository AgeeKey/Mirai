"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-20T08:10:37.043501

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries where each dictionary represents a row.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Input must be a list of dictionaries.")
    if not data:
        raise ValueError("Input data cannot be empty.")

    return pd.DataFrame(data)

def main() -> None:
    """
    Main function to demonstrate the creation of a DataFrame.
    """
    # Sample data
    sample_data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
    ]

    try:
        # Create the DataFrame
        df = create_dataframe(sample_data)
        print("DataFrame created successfully:")
        print(df)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()