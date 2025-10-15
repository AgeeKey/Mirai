"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T07:24:50.022096

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it into a DataFrame.

    Parameters:
    - file_path: str - Path to the CSV file.
    - column_names: Optional[list[str]] - List of column names to use. If None, uses default names.

    Returns:
    - pd.DataFrame: Processed DataFrame.

    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - pd.errors.EmptyDataError: If the file is empty.
    - pd.errors.ParserError: If there is an error parsing the file.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path, names=column_names, header=None if column_names else 'infer')
        
        # Basic data cleaning: drop rows with any missing values
        df.dropna(inplace=True)

        return df

    except FileNotFoundError as e:
        print(f"Error: The file at {file_path} was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: There was an error parsing the file.")
        raise e

def main():
    # Example usage of the load_and_process_data function
    file_path = 'data.csv'  # Specify the path to your CSV file
    column_names = ['Column1', 'Column2', 'Column3']

    try:
        data_frame = load_and_process_data(file_path, column_names)
        print(data_frame.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()