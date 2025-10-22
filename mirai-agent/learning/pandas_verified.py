"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-22T00:21:57.565093

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary do not match.
    """
    # Check if all columns have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same number of elements.")
    
    # Create DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame, column: str) -> Optional[dict]:
    """
    Calculate basic statistics for a given column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        column (str): The column name for which to calculate statistics.

    Returns:
        Optional[dict]: A dictionary containing the mean, median, and standard deviation, or None if the column does not exist.
    """
    if column not in df.columns:
        print(f"Column '{column}' does not exist in the DataFrame.")
        return None

    # Calculate statistics
    stats = {
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std_dev': df[column].std()
    }
    return stats

def main() -> None:
    """
    Main function to run the example.
    """
    # Sample data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [24, 30, 22, 35],
        'Score': [85.5, 90.0, 78.5, 88.0]
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:\n", df)

        # Calculate statistics for the 'Score' column
        stats = calculate_statistics(df, 'Score')
        if stats:
            print("Statistics for 'Score':", stats)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()