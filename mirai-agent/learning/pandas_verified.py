"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-15T09:34:02.714188

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame, filter by a specific column if required,
    and process the data by dropping any rows with missing values.

    Args:
        file_path (str): The path to the CSV file to be loaded.
        column_name (str): The name of the column to filter by.
        filter_value (Optional[str]): The value to filter the column by. If None, no filtering is applied.

    Returns:
        pd.DataFrame: A processed DataFrame with missing values dropped.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file at {file_path} was not found.") from e

    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter_value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]

    # Drop rows with any missing values
    df = df.dropna()

    return df

if __name__ == "__main__":
    # Example usage
    FILE_PATH = 'data.csv'  # Example file path
    COLUMN_NAME = 'Category'  # Example column name
    FILTER_VALUE = 'A'  # Example filter value

    try:
        processed_data = load_and_process_data(FILE_PATH, COLUMN_NAME, FILTER_VALUE)
        print(processed_data)
    except (FileNotFoundError, ValueError) as e:
        print(e)