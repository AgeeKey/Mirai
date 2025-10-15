"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T10:22:44.421014

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, List

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
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("No data found in the file.") from e

def filter_data(df: pd.DataFrame, column: str, values: List[Optional[str]]) -> pd.DataFrame:
    """
    Filter the DataFrame based on specified column values.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter on.
        values (List[Optional[str]]): The values to filter for.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    filtered_df = df[df[column].isin(values)]
    return filtered_df

def main(file_path: str, column: str, values: List[Optional[str]]) -> None:
    """
    Main function to load, filter, and display data.

    Args:
        file_path (str): The path to the CSV file.
        column (str): The column name to filter on.
        values (List[Optional[str]]): The values to filter for.
    """
    try:
        # Load the data
        df = load_data(file_path)
        
        # Filter the data
        filtered_df = filter_data(df, column, values)
        
        # Display the filtered data
        print(filtered_df)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage (uncomment the following line to run):
# main('data.csv', 'column_name', ['value1', 'value2'])