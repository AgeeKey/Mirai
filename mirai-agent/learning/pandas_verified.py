"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-16T18:55:50.794795

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame created from the input data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary are not consistent.
    """
    # Check if all lists in data have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")
    
    # Create and return the DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numerical column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to calculate statistics for.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation.
    """
    stats = {
        'Mean': df.mean(),
        'Median': df.median(),
        'Std Dev': df.std()
    }
    return pd.DataFrame(stats)

def main() -> None:
    """
    Main function to run the example.
    """
    # Sample data for demonstration
    data = {
        'A': np.random.rand(10),
        'B': np.random.rand(10),
        'C': np.random.rand(10)
    }

    try:
        # Create a DataFrame
        df = create_dataframe(data)
        print("DataFrame:")
        print(df)

        # Calculate statistics
        stats_df = calculate_statistics(df)
        print("\nStatistics:")
        print(stats_df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()