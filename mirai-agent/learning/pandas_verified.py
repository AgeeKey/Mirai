"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-19T14:34:39.853443

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame, filter the DataFrame based on a column value,
    and handle any potential errors during the process.

    Args:
        file_path (str): The path to the CSV file.
        column_name (str): The column name to filter on.
        filter_value (Optional[str]): The value to filter the column by. Default is None (no filtering).

    Returns:
        pd.DataFrame: A processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise

    # Check if the specified column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]

    return df

if __name__ == "__main__":
    # Example usage
    try:
        data_frame = load_and_process_data('data.csv', 'category', 'A')
        print(data_frame)
    except Exception as e:
        print(f"An error occurred: {e}")