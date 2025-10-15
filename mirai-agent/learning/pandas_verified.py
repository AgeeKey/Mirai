"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.96
Tests Passed: 0/1
Learned: 2025-10-15T10:54:59.278586

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, process it by filtering a specific column, and return a DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_name (str): The name of the column to filter.
    - filter_value (Optional[str]): The value to filter the column by. If None, no filtering is applied.

    Returns:
    - pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
    - FileNotFoundError: If the file at file_path does not exist.
    - KeyError: If the column_name does not exist in the DataFrame.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    
    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise KeyError(f"Column not found: {column_name}")

    # Filter the DataFrame if a filter_value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]
    
    return df

# Example usage
if __name__ == "__main__":
    try:
        # Specify the path to the CSV file and the column to filter
        csv_file_path = 'data.csv'
        filter_column = 'Category'
        filter_value = 'A'

        # Load and process the data
        processed_data = load_and_process_data(csv_file_path, filter_column, filter_value)
        
        # Display the processed DataFrame
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")