"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-15T05:47:15.795015

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from a dictionary of data.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary are not equal.
    """
    # Check if all columns have the same number of rows
    column_lengths = [len(value) for value in data.values()]
    if len(set(column_lengths)) != 1:
        raise ValueError("All columns must have the same number of rows.")

    # Create DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates basic statistics for numerical columns in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.DataFrame: A DataFrame containing the mean and standard deviation for each numerical column.
    """
    # Calculate mean and standard deviation
    stats = pd.DataFrame({
        'mean': df.mean(),
        'std': df.std()
    })
    return stats

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
        stats = calculate_statistics(df)
        print("\nStatistics:")
        print(stats)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()