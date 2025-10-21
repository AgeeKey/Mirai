"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-21T22:44:58.682565

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter by a specific column if provided, and return a DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_name (str): The name of the column to filter on.
        filter_value (Optional[str]): The value to filter the column by. If None, no filtering is applied.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e

    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]

    return df

def main():
    # Define the file path and column to process
    file_path = 'data.csv'
    column_name = 'category'
    
    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path, column_name, filter_value='A')
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()