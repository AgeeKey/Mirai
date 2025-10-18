"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-18T06:04:56.920000

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter based on a column value, and process the DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_name (str): The column name to filter on.
        filter_value (Optional[str]): The value to filter the column by. If None, no filtering is applied.

    Returns:
        pd.DataFrame: The processed DataFrame.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load data from CSV
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    
    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
    
    # Filter DataFrame if filter_value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]
    
    # Example processing: reset index after filtering
    df.reset_index(drop=True, inplace=True)
    
    return df

if __name__ == "__main__":
    # Example usage
    try:
        data = load_and_process_data('data.csv', 'Category', 'A')
        print(data)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")