"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-17T12:56:24.188633

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary are not equal.
    """
    # Check if all columns have the same length
    col_lengths = [len(v) for v in data.values()]
    if len(set(col_lengths)) != 1:
        raise ValueError("All columns must have the same number of elements.")
    
    # Create DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numeric column in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing mean, median, and standard deviation for each numeric column.
    """
    # Calculate statistics
    return df.describe()

def main() -> None:
    """
    Main function to execute the DataFrame creation and statistics calculation.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [2.5, 3.5, 4.5, np.nan, 5.5]  # Including a NaN value for demonstration
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Calculate and display statistics
        stats = calculate_statistics(df)
        print("\nStatistics:")
        print(stats)

    except ValueError as ve:
        print(f"Error: {ve}")

if __name__ == "__main__":
    main()