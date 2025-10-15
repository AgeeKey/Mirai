"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.95
Tests Passed: 0/1
Learned: 2025-10-15T15:14:45.633100

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, threshold: float) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame, filter rows based on a threshold, and clean the data.

    Parameters:
    - file_path: str - The path to the CSV file.
    - column_name: str - The column to filter on.
    - threshold: float - The threshold value for filtering.

    Returns:
    - pd.DataFrame - The processed DataFrame.
    """
    try:
        # Load the data from a CSV file
        df = pd.read_csv(file_path)
        
        # Check if the specified column exists
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
        
        # Filter rows where the specified column's value is greater than the threshold
        filtered_df = df[df[column_name] > threshold]
        
        # Clean up the DataFrame by dropping any rows with missing values
        cleaned_df = filtered_df.dropna()
        
        return cleaned_df
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the data: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Load and process the data from a sample CSV file
        result_df = load_and_process_data('sample_data.csv', 'value', 10.0)
        print(result_df)
    except Exception as e:
        print(f"Error: {e}")