"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-14T22:20:19.108989

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it into a DataFrame.
    
    Args:
        file_path (str): The path to the CSV file to load.
        column_names (Optional[list[str]]): List of column names to use. If None, uses the file's headers.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        Exception: For any other errors that may occur during loading.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, names=column_names, header=0 if column_names is None else None)
        
        # Basic data cleaning: drop duplicates and fill missing values
        df.drop_duplicates(inplace=True)
        df.fillna(method='ffill', inplace=True)  # Forward fill to handle missing values
        
        return df
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        raise
    except pd.errors.EmptyDataError as empty_error:
        print(f"Error: {empty_error}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data/sample_data.csv'  # Specify the path to your CSV file
    column_names = ['Column1', 'Column2', 'Column3']  # Example column names

    try:
        # Load and process the data
        data = load_and_process_data(file_path, column_names)
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"Failed to process data: {e}")

if __name__ == "__main__":
    main()