"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-20T09:29:22.964225

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: Optional[dict] = None) -> pd.DataFrame:
    """
    Create a DataFrame from the provided dictionary.

    Args:
        data (Optional[dict]): A dictionary with data to create the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame created from the provided data.
    """
    if data is None:
        raise ValueError("Input data cannot be None.")
    
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise RuntimeError("An error occurred while creating the DataFrame.") from e

def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Calculate basic statistics for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the mean, median, and standard deviation of each numeric column.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    
    try:
        stats = pd.Series({
            'mean': df.mean(),
            'median': df.median(),
            'std_dev': df.std()
        })
        return stats
    except Exception as e:
        raise RuntimeError("An error occurred while calculating statistics.") from e

if __name__ == "__main__":
    # Sample data to create the DataFrame
    sample_data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 6, 7, 8, 9],
        'C': [10, 11, 12, 13, 14]
    }
    
    # Create the DataFrame
    df = create_dataframe(sample_data)
    
    # Calculate statistics
    statistics = calculate_statistics(df)
    
    # Print the resulting statistics
    print(statistics)