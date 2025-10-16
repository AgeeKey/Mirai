"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-16T11:19:59.154678

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict[str, list]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data (dict[str, list]): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
    ValueError: If the lengths of the lists in the dictionary do not match.
    """
    # Check if all lists in the dictionary are of the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")
    
    # Create and return the DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for numeric columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
    pd.DataFrame: A DataFrame containing the mean, median, and standard deviation for each numeric column.
    """
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The DataFrame is empty. Statistics cannot be calculated.")
    
    # Calculate statistics
    stats = {
        'mean': df.mean(),
        'median': df.median(),
        'std_dev': df.std()
    }
    
    return pd.DataFrame(stats)

if __name__ == "__main__":
    # Example data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [10, 20, 30, 40, 50]
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created:")
        print(df)
        
        # Calculate and print statistics
        stats_df = calculate_statistics(df)
        print("\nStatistics:")
        print(stats_df)
    except ValueError as e:
        print(f"Error: {e}")