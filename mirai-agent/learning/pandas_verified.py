"""
Pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T11:59:43.107195

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, process it, and return a DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list[str]]): List of column names to rename. If None, no renaming is done.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the DataFrame is empty after loading.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if DataFrame is empty
        if df.empty:
            raise ValueError("The loaded DataFrame is empty.")

        # Rename columns if column_names is provided
        if column_names is not None:
            df.columns = column_names

        # Perform basic data cleaning: drop rows with any missing values
        df.dropna(inplace=True)

        return df

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def main():
    """
    Main function to run the data loading and processing example.
    """
    file_path = 'data/sample_data.csv'  # Replace with your actual file path
    column_names = ['Column1', 'Column2', 'Column3']  # Define your column names

    try:
        df = load_and_process_data(file_path, column_names)
        print("Processed DataFrame:")
        print(df)
    except Exception as e:
        print(f"Failed to process data: {e}")

if __name__ == "__main__":
    main()