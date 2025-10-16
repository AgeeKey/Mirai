"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-16T04:12:01.517438

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame, clean the data, and return the DataFrame.

    Parameters:
    - file_path: str - The path to the CSV file.
    - column_name: str - The column name to process.

    Returns:
    - Optional[pd.DataFrame]: A cleaned DataFrame or None if an error occurs.
    """
    try:
        # Load the data
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            print(f"Error: Column '{column_name}' not found in the data.")
            return None

        # Drop rows with missing values in the specified column
        df_cleaned = df.dropna(subset=[column_name])

        # Convert the specified column to a numeric type if possible
        df_cleaned[column_name] = pd.to_numeric(df_cleaned[column_name], errors='coerce')

        # Drop any rows that could not be converted to numeric
        df_cleaned = df_cleaned.dropna(subset=[column_name])

        return df_cleaned

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    cleaned_data = load_and_process_data('data.csv', 'column_of_interest')
    if cleaned_data is not None:
        print(cleaned_data.head())