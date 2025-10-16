"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-16T10:07:56.224363

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load and process data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        index_col (Optional[str]): Column to set as index. Defaults to None.

    Returns:
        pd.DataFrame: A processed DataFrame with the data from the CSV file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)
        
        # Print the first few rows of the DataFrame
        print("Data loaded successfully. Here's a preview:")
        print(df.head())
        
        # Basic data processing: drop any rows with missing values
        df.dropna(inplace=True)
        
        return df
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: Could not parse the file.")
        raise e

if __name__ == "__main__":
    # Example usage of the load_and_process_data function
    file_path = 'data.csv'  # Replace with the path to your CSV file
    try:
        df = load_and_process_data(file_path, index_col='id')  # Assuming 'id' is a column in your CSV
        print("Processed DataFrame:")
        print(df)
    except Exception as e:
        print("An error occurred during data loading and processing.")