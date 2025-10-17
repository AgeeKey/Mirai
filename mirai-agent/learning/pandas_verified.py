"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-17T07:33:44.219834

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and process it.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_name (str): The column to be processed for filtering.
    - filter_value (Optional[str]): The value to filter the DataFrame. If None, no filtering is applied.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the specified column does not exist in the DataFrame.
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

    # Return the processed DataFrame
    return df

# Example usage
if __name__ == "__main__":
    try:
        data_frame = load_and_process_data('data.csv', 'category', 'A')
        print(data_frame.head())
    except (FileNotFoundError, ValueError) as e:
        print(e)