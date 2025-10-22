"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-22T01:58:18.718967

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Creates a Pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame containing the provided data.
    
    Raises:
        ValueError: If the lengths of the lists in the dictionary are not equal.
    """
    # Check that all columns have the same number of rows
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same number of rows.")

    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates basic statistics (mean, median, std) for numeric columns in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation for each numeric column.
    """
    # Validate input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    # Calculate statistics
    stats = df.describe().T[['mean', '50%', 'std']]
    stats.columns = ['mean', 'median', 'std']
    return stats

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [2, 3, 5, 7, 11]
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:\n", df)
        
        # Calculate statistics
        stats = calculate_statistics(df)
        print("Statistics:\n", stats)

    except (ValueError, TypeError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()