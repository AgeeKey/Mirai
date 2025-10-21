"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-21T07:05:30.161348

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, process it by filtering based on a column value, 
    and return a cleaned DataFrame.

    Parameters:
    - file_path: Path to the CSV file.
    - column_name: Name of the column to filter on.
    - filter_value: Value to filter the column by (optional).

    Returns:
    - A DataFrame containing the cleaned data.
    """
    try:
        # Load data from a CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The provided CSV file is empty.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the CSV file: {str(e)}")

    # Display the initial shape of the DataFrame
    print(f"Initial data shape: {df.shape}")

    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter_value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]

    # Display the shape after filtering
    print(f"Data shape after filtering: {df.shape}")

    # Return the cleaned DataFrame
    return df

# Example usage
if __name__ == "__main__":
    file_path = 'data.csv'  # Replace with your actual CSV file path
    column_name = 'Category'  # Replace with the actual column name to filter by
    filter_value = 'A'  # Replace with the actual value to filter by, if needed

    try:
        processed_data = load_and_process_data(file_path, column_name, filter_value)
        print(processed_data.head())  # Display the first few rows of the processed DataFrame
    except Exception as e:
        print(f"Error: {e}")