"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-22T16:44:21.467179

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and perform basic data processing.

    Args:
        file_path (str): The path to the CSV file.
        index_col (Optional[str]): Column to set as index (default is None).

    Returns:
        pd.DataFrame: Processed DataFrame.
    
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file cannot be parsed.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)
        
        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Reset index if no index column is provided
        if index_col is None:
            df.reset_index(drop=True, inplace=True)
        
        return df

    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: The file could not be parsed.")
        raise e

if __name__ == "__main__":
    # Example usage of the load_and_process_data function
    try:
        df = load_and_process_data('data.csv', index_col='id')
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")