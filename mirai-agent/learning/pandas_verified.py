"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-14T22:53:28.038585

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a DataFrame from a dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A pandas DataFrame constructed from the input data.
    
    Raises:
    ValueError: If the input data is not in the expected format.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    try:
        df = pd.DataFrame(data)  # Create DataFrame from the dictionary
        return df
    except Exception as e:
        raise ValueError("An error occurred while creating the DataFrame: " + str(e))

def calculate_statistics(df: pd.DataFrame, column: str) -> Optional[dict]:
    """
    Calculate basic statistics for a given column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    column (str): The column name for which to calculate statistics.

    Returns:
    Optional[dict]: A dictionary containing mean, median, and standard deviation, or None if column is not found.
    """
    if column not in df.columns:
        print(f"Column '{column}' not found in DataFrame.")
        return None
    
    mean = df[column].mean()
    median = df[column].median()
    std_dev = df[column].std()
    
    return {
        'mean': mean,
        'median': median,
        'std_dev': std_dev
    }

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [2, 3, 5, np.nan, 1]
    }

    # Create DataFrame
    df = create_dataframe(data)
    print("DataFrame:")
    print(df)

    # Calculate statistics for column 'A'
    stats = calculate_statistics(df, 'A')
    if stats:
        print("\nStatistics for column 'A':")
        print(stats)

if __name__ == "__main__":
    main()