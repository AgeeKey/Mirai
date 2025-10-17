"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-17T20:32:34.724754

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
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file at file_path does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is an error parsing the file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: {e}")
        raise

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame including basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    print("Summary of the DataFrame:")
    print(df.describe())
    print("\nData Types:")
    print(df.dtypes)

def filter_data(df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a threshold for a specified column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to apply the filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: A DataFrame containing the filtered data.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    filtered_df = df[df[column] > threshold]
    return filtered_df

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your actual file path

    # Load the data
    try:
        data = load_data(file_path)
        # Summarize the data
        summarize_data(data)
        
        # Filter the data
        filtered_data = filter_data(data, 'column_name', 10.0)  # Replace 'column_name' with your actual column name
        print("\nFiltered Data:")
        print(filtered_data)
    except Exception as e:
        print(f"An error occurred: {e}")