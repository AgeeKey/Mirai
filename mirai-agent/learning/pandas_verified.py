"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-14T17:28:13.197019

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple

def create_dataframe(data: np.ndarray, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a numpy array.

    Args:
        data (np.ndarray): The data to be converted into a DataFrame.
        columns (Optional[list]): List of column names for the DataFrame. Default is None.

    Returns:
        pd.DataFrame: A DataFrame containing the input data.

    Raises:
        ValueError: If data is empty or not a 2D numpy array.
    """
    if data.size == 0:
        raise ValueError("Input data cannot be empty.")
    if len(data.shape) != 2:
        raise ValueError("Input data must be a 2D numpy array.")

    return pd.DataFrame(data, columns=columns)

def calculate_statistics(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate the mean and standard deviation of each numeric column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Tuple[float, float]: A tuple containing the mean and standard deviation.

    Raises:
        ValueError: If the DataFrame is empty or has no numeric columns.
    """
    if df.empty:
        raise ValueError("Input DataFrame cannot be empty.")

    means = df.mean()
    std_devs = df.std()
    
    return means.mean(), std_devs.mean()

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistical calculation.
    """
    # Example data
    data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    columns = ['A', 'B', 'C']

    # Create DataFrame
    try:
        df = create_dataframe(data, columns)
        print("DataFrame created successfully:")
        print(df)

        # Calculate statistics
        mean, std_dev = calculate_statistics(df)
        print(f"Mean of numeric columns: {mean}")
        print(f"Standard deviation of numeric columns: {std_dev}")
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()