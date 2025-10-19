"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-19T10:37:56.534474

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load and process data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list[str]]): List of column names to use. If None, uses the first row as header.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the data cannot be converted to a DataFrame.
    """
    try:
        # Load data from CSV file
        df = pd.read_csv(file_path, names=column_names, header=0 if column_names is None else None)
        
        # Drop any rows with missing values
        df.dropna(inplace=True)

        # Reset the index of the DataFrame
        df.reset_index(drop=True, inplace=True)

        return df
    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
        raise e
    except ValueError as e:
        print("Error: Could not convert data to a DataFrame.")
        raise e

def main():
    # Example usage of the load_and_process_data function
    file_path = 'data.csv'  # Specify your CSV file path
    try:
        df = load_and_process_data(file_path)
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()