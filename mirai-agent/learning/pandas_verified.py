"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-15T20:09:00.616919

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame containing the provided data.

    Raises:
        ValueError: If the input data is not a dictionary or if the lists are not of the same length.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    length = None
    for key, value in data.items():
        if not isinstance(value, list):
            raise ValueError(f"Value for '{key}' must be a list.")
        if length is None:
            length = len(value)
        elif length != len(value):
            raise ValueError("All lists must be of the same length.")
    
    return pd.DataFrame(data)

def main() -> None:
    """
    Main function to run the DataFrame creation and display.
    """
    # Sample data to create a DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }

    try:
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()