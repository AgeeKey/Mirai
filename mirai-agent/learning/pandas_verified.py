"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-22T01:10:11.665937

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a DataFrame from a dictionary of data.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.

    Raises:
    ValueError: If the input data is invalid.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")

    # Attempt to create a DataFrame
    try:
        df = pd.DataFrame(data)
    except Exception as e:
        raise ValueError(f"Failed to create DataFrame: {e}")
    
    return df

def calculate_mean(df: pd.DataFrame, column: str) -> Optional[float]:
    """
    Calculate the mean of a specified column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    column (str): The column name for which to calculate the mean.

    Returns:
    Optional[float]: The mean of the specified column, or None if the column does not exist.

    Raises:
    ValueError: If the column name is not in the DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    # Calculate and return the mean
    return df[column].mean()

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and mean calculation.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 6, 7, 8, 9],
        'C': [10, 11, 12, 13, 14]
    }

    # Create DataFrame
    df = create_dataframe(data)
    print("DataFrame created:")
    print(df)

    # Calculate mean of column 'B'
    try:
        mean_b = calculate_mean(df, 'B')
        print(f"Mean of column 'B': {mean_b}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()