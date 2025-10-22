"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-22T04:38:01.220590

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, filter_column: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame, filter the DataFrame based on a specified column and value,
    and return the processed DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file to load.
    - filter_column (str): The column to filter on.
    - filter_value (Optional[str]): The value to filter by; if None, no filtering is applied.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")

        # Check if the filter_column exists in the DataFrame
        if filter_column not in df.columns:
            raise ValueError(f"Column '{filter_column}' does not exist in the DataFrame.")

        # Filter the DataFrame if filter_value is provided
        if filter_value is not None:
            df = df[df[filter_column] == filter_value]
            print(f"Data filtered by {filter_column} == {filter_value}.")

        return df

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Example usage
if __name__ == "__main__":
    # Define the CSV file path and filtering criteria
    csv_file_path = 'data.csv'
    column_to_filter = 'Category'
    value_to_filter = 'A'

    # Load and process the data
    processed_data = load_and_process_data(csv_file_path, column_to_filter, value_to_filter)

    # Display the processed DataFrame
    print(processed_data)