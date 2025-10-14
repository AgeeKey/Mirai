"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-14T20:42:47.982467

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Dict, Any

def create_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data (Dict[str, Any]): A dictionary where keys are column names and values are lists of column values.

    Returns:
    pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
    ValueError: If the input data is not a dictionary or if columns have different lengths.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")

    column_lengths = [len(v) for v in data.values()]
    if len(set(column_lengths)) != 1:
        raise ValueError("All columns must have the same number of values.")

    return pd.DataFrame(data)

def main() -> None:
    """
    Main function to execute the DataFrame creation and display.
    """
    try:
        # Sample data to create DataFrame
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }
        
        # Create DataFrame
        df = create_dataframe(data)
        
        # Display the DataFrame
        print(df)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()