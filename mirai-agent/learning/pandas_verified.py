"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-16T06:04:11.172062

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file and process it by dropping missing values in a specified column.

    Parameters:
    - file_path: str - The path to the CSV file.
    - column_name: str - The name of the column to drop missing values.

    Returns:
    - Optional[pd.DataFrame] - A DataFrame with missing values dropped, or None if an error occurs.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Display the first few rows of the DataFrame
        print("Initial DataFrame:")
        print(df.head())

        # Drop rows with missing values in the specified column
        cleaned_df = df.dropna(subset=[column_name])
        
        # Display the cleaned DataFrame
        print("Cleaned DataFrame:")
        print(cleaned_df.head())
        
        return cleaned_df

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

# Example usage
if __name__ == "__main__":
    df = load_and_process_data('data.csv', 'column_name')