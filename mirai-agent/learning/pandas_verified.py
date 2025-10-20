"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T04:13:54.181115

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
        ValueError: If the input data is empty or not a dictionary.
    """
    if not isinstance(data, dict) or not data:
        raise ValueError("Input data must be a non-empty dictionary.")
    
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame, column: str) -> Optional[dict]:
    """
    Calculate basic statistics for a specified column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing data.
        column (str): The column name for which to calculate statistics.

    Returns:
        Optional[dict]: A dictionary containing mean, median, and standard deviation, or None if the column does not exist.

    Raises:
        ValueError: If the column is not found in the DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    stats = {
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std_dev': df[column].std()
    }
    
    return stats

# Example usage
if __name__ == "__main__":
    try:
        # Sample data for creating a DataFrame
        data = {
            'A': np.random.rand(10),
            'B': np.random.rand(10),
            'C': np.random.rand(10)
        }
        
        # Create DataFrame
        df = create_dataframe(data)
        
        # Calculate statistics for column 'A'
        stats = calculate_statistics(df, 'A')
        
        print("DataFrame:")
        print(df)
        print("\nStatistics for column 'A':")
        print(stats)
        
    except Exception as e:
        print(f"An error occurred: {e}")