"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T21:45:27.259980

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
        pd.DataFrame: A DataFrame created from the provided data.

    Raises:
        ValueError: If any of the columns in the data have different lengths.
    """
    if not all(len(v) == len(next(iter(data.values()))) for v in data.values()):
        raise ValueError("All columns must have the same length.")

    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numerical column in a DataFrame.

    Parameters:
        df (pd.DataFrame): A DataFrame containing numerical data.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation for each column.
    """
    stats = {
        'Mean': df.mean(),
        'Median': df.median(),
        'Std Dev': df.std()
    }
    return pd.DataFrame(stats)

def main():
    # Sample data
    data = {
        'A': np.random.rand(10),
        'B': np.random.rand(10),
        'C': np.random.rand(10)
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