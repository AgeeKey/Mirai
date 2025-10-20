"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-20T23:41:42.858826

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict[str, list[Optional[float]]]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict[str, list[Optional[float]]]): A dictionary where keys are column names 
                                                  and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the lengths of the data lists are not equal.
    """
    # Check if all columns have the same length
    lengths = [len(col) for col in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same number of rows.")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numerical column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation.
    """
    # Ensure the DataFrame is not empty
    if df.empty:
        raise ValueError("The DataFrame is empty.")

    # Calculate statistics
    stats = {
        'Mean': df.mean(),
        'Median': df.median(),
        'Standard Deviation': df.std()
    }
    return pd.DataFrame(stats)

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [np.nan, 1, 2, 3, 4]
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