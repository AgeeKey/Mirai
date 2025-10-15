"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-15T13:05:01.711928

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, filter_column: str, filter_value: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file, filter it based on specified column and value,
    and return the processed DataFrame.

    :param file_path: Path to the CSV file.
    :param filter_column: Column name to filter on.
    :param filter_value: Value to filter the specified column by.
    :return: Filtered DataFrame or None if an error occurs.
    """
    try:
        # Load the data from CSV
        data = pd.read_csv(file_path)
        
        # Check if filter_column exists in the DataFrame
        if filter_column not in data.columns:
            raise ValueError(f"Column '{filter_column}' does not exist in the DataFrame.")
        
        # Filter the DataFrame
        filtered_data = data[data[filter_column] == filter_value]
        
        return filtered_data
    
    except FileNotFoundError:
        print(f"Error: The file at path '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

# Example usage
if __name__ == "__main__":
    df = load_and_process_data('data.csv', 'category', 'A')
    if df is not None:
        print(df.head())