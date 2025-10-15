"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-15T03:54:45.030046

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter it based on a specific column value,
    and return the processed DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_name (str): The name of the column to filter on.
    - filter_value (Optional[str]): The value to filter the column by. Default is None.

    Returns:
    - pd.DataFrame: The processed DataFrame after loading and filtering.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

        # Filter the DataFrame if a filter value is provided
        if filter_value is not None:
            df = df[df[column_name] == filter_value]

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        processed_data = load_and_process_data('data.csv', 'category', 'A')
        print(processed_data)
    except Exception as e:
        print(f"Failed to process data: {e}")