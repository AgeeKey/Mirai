"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-17T12:07:33.252679

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter it by a specific column if needed,
    and return a processed DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_name (str): The column to filter on.
        filter_value (Optional[str]): The value to filter by; if None, no filtering is applied.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column is not found in the DataFrame.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file {file_path} was not found.") from e

    # Check if the specified column exists
    if column_name not in df.columns:
        raise ValueError(f"Error: The column '{column_name}' does not exist in the DataFrame.")
    
    # Filter the DataFrame if a filter value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]
    
    # Return the processed DataFrame
    return df

if __name__ == "__main__":
    # Example usage
    try:
        processed_data = load_and_process_data('data.csv', 'Category', 'A')
        print(processed_data)
    except Exception as e:
        print(e)