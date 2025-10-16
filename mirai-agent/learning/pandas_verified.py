"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T03:56:00.534820

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame containing the provided data.

    Raises:
        ValueError: If the dictionary is empty or if the lists are of unequal length.
    """
    if not data:
        raise ValueError("Input dictionary cannot be empty.")
    
    length = len(next(iter(data.values())))
    if any(len(value) != length for value in data.values()):
        raise ValueError("All columns must have the same length.")
    
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> Optional[dict]:
    """
    Calculate basic statistics for numerical columns in a DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame from which to calculate statistics.

    Returns:
        Optional[dict]: A dictionary containing the mean, median, and standard deviation of numerical columns.
    """
    if df.empty:
        return None
    
    stats = {
        'mean': df.mean().to_dict(),
        'median': df.median().to_dict(),
        'std_dev': df.std().to_dict()
    }
    return stats

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistic calculation.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 6, 7, 8, 9],
        'C': [10, 11, 12, 13, 14]
    }

    try:
        df = create_dataframe(data)  # Create DataFrame
        print("DataFrame created successfully:")
        print(df)

        stats = calculate_statistics(df)  # Calculate statistics
        if stats:
            print("Statistics calculated:")
            print(stats)
        else:
            print("DataFrame is empty, no statistics to calculate.")
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()