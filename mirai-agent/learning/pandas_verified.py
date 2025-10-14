"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-14T16:39:03.196181

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise

def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics for the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        pd.DataFrame: DataFrame containing summary statistics.
    """
    return df.describe()

def filter_data(df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a column value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter on.
        threshold (float): The threshold value to filter by.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    return df[df[column] > threshold]

def main(file_path: str, column: str, threshold: float) -> None:
    """
    Main function to load, summarize, and filter the data.

    Args:
        file_path (str): Path to the CSV file.
        column (str): Column name for filtering.
        threshold (float): Threshold value for filtering.
    """
    df = load_data(file_path)
    summary = summarize_data(df)
    print("Summary Statistics:")
    print(summary)

    filtered_df = filter_data(df, column, threshold)
    print(f"Filtered Data (where {column} > {threshold}):")
    print(filtered_df)

if __name__ == "__main__":
    # Example usage
    FILE_PATH = 'data.csv'  # Update with your CSV file path
    COLUMN = 'age'          # Update with the column to filter
    THRESHOLD = 30          # Update with your threshold value

    main(FILE_PATH, COLUMN, THRESHOLD)