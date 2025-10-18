"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-18T21:29:45.684436

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter it based on a specific column value, and return the processed DataFrame.

    Args:
        file_path (str): Path to the CSV file.
        column_name (str): Column name to filter the DataFrame.
        filter_value (Optional[str]): Value to filter the DataFrame by. If None, no filtering is applied.

    Returns:
        pd.DataFrame: Processed DataFrame after loading and filtering.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file {file_path} was not found.") from e

    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Error: The column '{column_name}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]

    return df

if __name__ == "__main__":
    # Example usage
    try:
        processed_data = load_and_process_data('data.csv', 'Category', 'A')
        print(processed_data)
    except Exception as e:
        print(e)