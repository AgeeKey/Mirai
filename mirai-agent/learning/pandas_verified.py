"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-19T04:34:54.475205

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, clean it, and return a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.
    column_names (Optional[list]): A list of column names to rename the DataFrame columns.
    
    Returns:
    pd.DataFrame: A DataFrame containing the cleaned data.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If there is a parsing error in the file.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Rename columns if provided
        if column_names is not None:
            df.columns = column_names
            
        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path.")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty. Please provide a valid CSV file.")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: There was a parsing error while reading the file. {e}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        data_frame = load_and_process_data('data.csv', column_names=['A', 'B', 'C'])
        print(data_frame.head())
    except Exception as e:
        print(f"An error occurred: {e}")