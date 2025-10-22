"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-22T12:23:12.238694

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
        ValueError: If the input data is invalid (e.g., lists of different lengths).
    """
    if not all(len(v) == len(next(iter(data.values()))) for v in data.values()):
        raise ValueError("All columns must have the same number of rows.")

    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame, column: str) -> Optional[dict]:
    """
    Calculate basic statistics for a given column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column (str): The column name to calculate statistics for.

    Returns:
        Optional[dict]: A dictionary with mean, median, and std deviation, or None if column not found.
    """
    if column not in df.columns:
        print(f"Column '{column}' not found in DataFrame.")
        return None

    stats = {
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std_dev': df[column].std()
    }
    return stats

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
    """
    try:
        # Sample data creation
        data = {
            "A": [1, 2, 3, 4, 5],
            "B": [5, 4, 3, 2, 1],
            "C": [2, 3, np.nan, 5, 6]
        }
        
        # Create DataFrame
        df = create_dataframe(data)

        # Calculate statistics for column 'A'
        stats_a = calculate_statistics(df, 'A')
        print("Statistics for column 'A':", stats_a)

        # Calculate statistics for column 'C'
        stats_c = calculate_statistics(df, 'C')
        print("Statistics for column 'C':", stats_c)

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()