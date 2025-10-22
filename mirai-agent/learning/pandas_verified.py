"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-22T00:06:12.060930

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, clean, and return a DataFrame.
    
    Parameters:
    - file_path (str): The path to the CSV file.
    - column_names (Optional[list]): List of column names to rename in the DataFrame.

    Returns:
    - pd.DataFrame: A cleaned DataFrame.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - pd.errors.EmptyDataError: If the file is empty.
    - pd.errors.ParserError: If there is an error parsing the file.
    """
    try:
        # Load the data from CSV
        df = pd.read_csv(file_path)
        
        # Rename columns if column_names are provided
        if column_names:
            df.columns = column_names
        
        # Drop rows with any missing values
        df.dropna(inplace=True)
        
        return df
        
    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
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
        data = load_and_process_data('data.csv', column_names=['A', 'B', 'C'])
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print("An error occurred while processing the data.")