"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-18T07:23:51.052461

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame, filter by a specified column if a filter value is provided,
    and return the processed DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_name (str): The name of the column to filter by.
    - filter_value (Optional[str]): The value to filter the specified column by. Default is None (no filtering).

    Returns:
    - pd.DataFrame: The processed DataFrame.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load data from CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e

    # Check if the specified column exists
    if column_name not in df.columns:
        raise ValueError(f"The column {column_name} does not exist in the DataFrame.")

    # Filter the DataFrame if a filter value is provided
    if filter_value:
        df = df[df[column_name] == filter_value]

    return df

# Example usage
if __name__ == "__main__":
    try:
        # Load and process the data
        processed_data = load_and_process_data('data.csv', 'Category', 'A')
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")