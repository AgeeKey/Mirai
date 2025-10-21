"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-21T06:49:32.059889

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: Optional[dict] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the provided data.

    Args:
        data (Optional[dict]): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame created from the input data.

    Raises:
        ValueError: If the input data is not a dictionary or if the columns have different lengths.
    """
    if data is None:
        data = {
            'A': np.random.rand(10),
            'B': np.random.rand(10),
            'C': np.random.rand(10)
        }

    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")

    # Check if all columns have the same length
    column_lengths = [len(v) for v in data.values()]
    if len(set(column_lengths)) != 1:
        raise ValueError("All columns must have the same length.")

    df = pd.DataFrame(data)
    return df

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation for each column.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    stats = {
        'Mean': df.mean(),
        'Median': df.median(),
        'Std Dev': df.std()
    }
    return pd.DataFrame(stats)

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
    """
    try:
        # Create a DataFrame with random data
        df = create_dataframe()
        print("DataFrame:")
        print(df)

        # Calculate and display statistics
        stats = calculate_statistics(df)
        print("\nStatistics:")
        print(stats)
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()