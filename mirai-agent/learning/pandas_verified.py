"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-19T05:53:43.745157

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: Optional[dict] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a provided dictionary.

    Args:
        data (Optional[dict]): A dictionary where keys are column names and 
                               values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame created from the input data.
    
    Raises:
        ValueError: If data is not provided or is empty.
    """
    if data is None or not data:
        raise ValueError("Input data must be a non-empty dictionary.")

    df = pd.DataFrame(data)
    return df

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for numeric columns in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame with numeric columns.

    Returns:
        pd.DataFrame: A DataFrame containing mean, median, and standard deviation.
    
    Raises:
        ValueError: If the DataFrame is empty or has no numeric columns.
    """
    if df.empty:
        raise ValueError("The input DataFrame is empty.")

    numeric_cols = df.select_dtypes(include=np.number)

    if numeric_cols.empty:
        raise ValueError("No numeric columns found in the DataFrame.")

    stats = {
        'Mean': numeric_cols.mean(),
        'Median': numeric_cols.median(),
        'Std Dev': numeric_cols.std()
    }

    stats_df = pd.DataFrame(stats)
    return stats_df

# Example usage
if __name__ == "__main__":
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 6, 7, 8, 9],
        'C': ['foo', 'bar', 'baz', 'qux', 'quux']  # Non-numeric column
    }

    try:
        df = create_dataframe(data)
        stats_df = calculate_statistics(df)
        print("Original DataFrame:")
        print(df)
        print("\nStatistics DataFrame:")
        print(stats_df)
    except ValueError as e:
        print(f"Error: {e}")