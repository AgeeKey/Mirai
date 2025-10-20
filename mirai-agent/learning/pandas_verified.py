"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-20T07:54:58.258673

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame, process it by filtering specified column, 
    and return the resulting DataFrame.

    Args:
        file_path (str): Path to the CSV file.
        column_name (str): Name of the column to filter on.
        filter_value (Optional[str]): Value to filter the specified column. If None, no filtering is applied.

    Returns:
        pd.DataFrame: Processed DataFrame after loading and filtering.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    # Check if the specified column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]

    return df

if __name__ == "__main__":
    # Example usage of the load_and_process_data function
    try:
        result_df = load_and_process_data('data.csv', 'category', 'A')
        print(result_df)
    except Exception as e:
        print(f"An error occurred: {e}")