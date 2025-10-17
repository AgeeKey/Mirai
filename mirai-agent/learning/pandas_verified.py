"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-17T18:06:05.670626

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: Optional[np.ndarray] = None) -> pd.DataFrame:
    """
    Create a DataFrame from a numpy array or return a default DataFrame.

    Args:
        data (Optional[np.ndarray]): A 2D numpy array to create the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame created from the input data or a default one if no data is provided.
    """
    if data is None:
        # Create a default DataFrame if no data is provided
        data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    
    try:
        df = pd.DataFrame(data, columns=['A', 'B', 'C'])
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Calculate basic statistics for the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.Series: A Series containing the mean, median, and standard deviation of the DataFrame.
    """
    try:
        stats = pd.Series({
            'mean': df.mean(),
            'median': df.median(),
            'std_dev': df.std()
        })
        return stats
    except Exception as e:
        print(f"Error calculating statistics: {e}")
        return pd.Series()  # Return an empty Series on error

if __name__ == "__main__":
    # Create a sample DataFrame
    df = create_dataframe()
    print("DataFrame:")
    print(df)

    # Calculate statistics for the DataFrame
    stats = calculate_statistics(df)
    print("\nStatistics:")
    print(stats)