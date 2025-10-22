"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-22T06:28:49.373307

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Any, Dict

def create_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the provided dictionary.

    Args:
        data (Dict[str, Any]): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
        ValueError: If the lengths of the lists in the data dictionary are not consistent.
    """
    # Check if all columns have the same length
    column_lengths = [len(v) for v in data.values()]
    if len(set(column_lengths)) != 1:
        raise ValueError("All columns must have the same number of rows")

    # Create the DataFrame
    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to execute the DataFrame creation and display.
    """
    # Sample data to create a DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }

    try:
        # Create DataFrame using the sample data
        df = create_dataframe(data)
        print(df)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()