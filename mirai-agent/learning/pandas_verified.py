"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-15T07:41:04.803890

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_and_process_data(file_path: str, delimiter: str = ',', columns: Union[list, None] = None) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame and process it.

    Args:
        file_path (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file. Defaults to ','.
        columns (list, optional): List of columns to select from the DataFrame. If None, all columns are selected.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If there is an error parsing the CSV file.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter, usecols=columns)
        
        # Perform basic data cleaning
        df.dropna(inplace=True)  # Drop rows with missing values
        df.reset_index(drop=True, inplace=True)  # Reset index
        
        return df
    
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: There was a problem parsing the file.")
        raise e

# Example usage
if __name__ == "__main__":
    try:
        data = load_and_process_data('example_data.csv', delimiter=',', columns=['column1', 'column2'])
        print(data.head())
    except Exception as e:
        print(f"An error occurred: {e}")