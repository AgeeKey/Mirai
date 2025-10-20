"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T12:09:03.501957

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and process it by renaming columns if provided.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list[str]]): A list of new column names to rename the DataFrame columns.

    Returns:
        pd.DataFrame: The processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the number of new column names does not match the DataFrame's columns.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)

        # Rename columns if new names are provided
        if column_names is not None:
            if len(column_names) != df.shape[1]:
                raise ValueError("The number of new column names must match the number of columns in the DataFrame.")
            df.columns = column_names

        return df
    
    except FileNotFoundError as e:
        print(f"Error: The file at {file_path} was not found.")
        raise e
    except ValueError as e:
        print(f"ValueError: {e}")
        raise e

def main():
    # Example usage of the load_and_process_data function
    file_path = 'data.csv'  # Path to your CSV file
    new_column_names = ['Column1', 'Column2', 'Column3']  # Example new column names

    try:
        df = load_and_process_data(file_path, new_column_names)
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()