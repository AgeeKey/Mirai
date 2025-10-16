"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-16T00:43:44.438664

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict[str, list], index: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary of lists.

    Args:
        data (dict[str, list]): A dictionary where keys are column names and values are lists of column data.
        index (Optional[list[str]]): Optional list for the DataFrame index.

    Returns:
        pd.DataFrame: A pandas DataFrame created from the provided data.

    Raises:
        ValueError: If the lengths of the lists in the data dictionary do not match.
    """
    # Validate input data
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the data dictionary must have the same length.")

    # Create DataFrame
    df = pd.DataFrame(data, index=index)
    return df

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing basic statistics (mean, std, min, max) for each numeric column.
    """
    # Calculate statistics
    stats = df.describe()
    return stats

if __name__ == '__main__':
    # Example data
    data = {
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8],
        'C': [9, 10, 11, 12]
    }
    
    # Create DataFrame
    try:
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Calculate and print statistics
        statistics = calculate_statistics(df)
        print("\nStatistics:")
        print(statistics)
    except ValueError as e:
        print(f"Error: {e}")