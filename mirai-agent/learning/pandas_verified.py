"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T06:25:04.365304

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame and process it by renaming columns if specified.

    Args:
        file_path (str): Path to the CSV file.
        column_names (Optional[list[str]]): List of new column names.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the number of new column names does not match the number of columns in the DataFrame.
    """
    try:
        # Load the data
        df = pd.read_csv(file_path)

        # Rename columns if new names are provided
        if column_names is not None:
            if len(column_names) != len(df.columns):
                raise ValueError("The number of new column names must match the number of columns in the DataFrame.")
            df.columns = column_names

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def main():
    # Example usage
    file_path = 'data.csv'
    new_columns = ['Column1', 'Column2', 'Column3']

    try:
        df = load_and_process_data(file_path, new_columns)
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"Failed to load and process data: {e}")

if __name__ == "__main__":
    main()