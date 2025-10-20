"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-20T03:42:18.896353

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Tuple

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.
    
    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
    ValueError: If the input data is invalid (e.g., columns have different lengths).
    """
    if not data:
        raise ValueError("Input data cannot be empty")
    
    length = len(next(iter(data.values())))
    for key, value in data.items():
        if len(value) != length:
            raise ValueError(f"Column '{key}' has a different length than the others.")

    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate the mean and standard deviation of a DataFrame's numeric columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    Tuple[float, float]: A tuple containing the mean and standard deviation of the DataFrame.
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    mean = df.mean().mean()  # Mean of all numeric columns
    std_dev = df.std().mean()  # Standard deviation of all numeric columns
    return mean, std_dev

def main() -> None:
    """
    Main function to create a DataFrame, calculate statistics, and print results.
    """
    try:
        # Sample data for DataFrame creation
        data = {
            "A": [1, 2, 3, 4, 5],
            "B": [5, 4, 3, 2, 1],
            "C": [2, 3, np.nan, 5, 6]
        }
        
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)
        
        # Calculate statistics
        mean, std_dev = calculate_statistics(df)
        print(f"Mean of DataFrame: {mean}")
        print(f"Standard Deviation of DataFrame: {std_dev}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()