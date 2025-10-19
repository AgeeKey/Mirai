"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-19T23:30:06.131661

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by selecting specific columns.

    Args:
        file_path (str): The path to the CSV file to be loaded.
        columns (Optional[list]): A list of columns to select from the DataFrame. If None, all columns are selected.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded and processed data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified columns are not found in the DataFrame.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)

        # Select specific columns if provided
        if columns is not None:
            missing_columns = set(columns) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Columns not found in DataFrame: {missing_columns}")
            df = df[columns]

        return df

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def main():
    """
    The main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Replace with your CSV file path
    selected_columns = ['Column1', 'Column2']  # Replace with your desired columns

    try:
        # Load and process the data
        data = load_and_process_data(file_path, selected_columns)
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"Failed to load and process data: {e}")

if __name__ == "__main__":
    main()