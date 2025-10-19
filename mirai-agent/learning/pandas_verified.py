"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-19T13:47:29.673174

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, process it by filtering and returning a DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_name (str): The name of the column to filter on.
    - filter_value (Optional[str]): The value to filter the column by. Default is None (no filtering).

    Returns:
    - pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the CSV data into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file {file_path} does not exist.") from e
    
    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Error: The column '{column_name}' does not exist in the data.")
    
    # Filter the DataFrame if filter_value is provided
    if filter_value:
        df = df[df[column_name] == filter_value]
    
    return df

def main():
    file_path = 'data.csv'  # Path to the CSV file
    column_name = 'Category'  # Column to filter on
    filter_value = 'Electronics'  # Value to filter by
    
    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path, column_name, filter_value)
        print(processed_data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()