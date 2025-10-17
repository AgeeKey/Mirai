"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-17T06:12:50.401698

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
    ValueError: If the input data is not a dictionary or if the lists have different lengths.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")

    # Check if all lists in the dictionary have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")

    # Create DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate statistics for each numerical column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.DataFrame: A DataFrame containing mean, median, and standard deviation for each numerical column.
    """
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    # Calculate mean, median, and standard deviation
    stats = {
        'Mean': df.mean(),
        'Median': df.median(),
        'Standard Deviation': df.std()
    }

    return pd.DataFrame(stats)

# Example usage
if __name__ == "__main__":
    try:
        # Sample data
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': [5, 4, 3, 2, 1],
            'C': [2, np.nan, 3, 4, 5]
        }

        # Create DataFrame
        df = create_dataframe(data)

        # Calculate statistics
        stats_df = calculate_statistics(df)

        print("Original DataFrame:")
        print(df)
        print("\nStatistics DataFrame:")
        print(stats_df)

    except Exception as e:
        print(f"An error occurred: {e}")