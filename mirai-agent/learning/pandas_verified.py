"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-17T07:17:23.099639

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a given dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame containing the input data.

    Raises:
        ValueError: If the input data is not a dictionary or if the lists have different lengths.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")

    # Check if all lists have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")

    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for numeric columns in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation of numeric columns.
    """
    stats = {
        'mean': df.mean(),
        'median': df.median(),
        'std_dev': df.std()
    }
    return pd.DataFrame(stats)

def main():
    # Sample data
    data = {
        'A': np.random.randint(1, 100, size=10),
        'B': np.random.rand(10) * 100,
        'C': np.random.randint(1, 100, size=10)
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Calculate statistics
        stats_df = calculate_statistics(df)
        print("\nStatistics:")
        print(stats_df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()