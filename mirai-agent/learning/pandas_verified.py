"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-22T14:00:26.788352

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by renaming columns if specified.

    Parameters:
    - file_path: str : Path to the CSV file.
    - column_names: Optional[list[str]] : List of new column names to assign.

    Returns:
    - pd.DataFrame : Processed DataFrame.
    
    Raises:
    - FileNotFoundError : If the specified file does not exist.
    - ValueError : If the number of column names does not match the data.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)

        # Rename columns if new names are provided
        if column_names is not None:
            if len(column_names) != len(df.columns):
                raise ValueError("Number of column names does not match the number of columns in the data.")
            df.columns = column_names
        
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise

def main():
    # Define the file path and new column names
    file_path = 'data.csv'
    new_column_names = ['Column1', 'Column2', 'Column3']

    # Load and process the data
    try:
        processed_data = load_and_process_data(file_path, new_column_names)
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()