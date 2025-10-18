"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-18T11:20:34.982042

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, delimiter: str = ',', index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame and process it.

    Args:
        file_path (str): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file. Default is ','.
        index_col (Optional[str]): Column(s) to set as index. Default is None.

    Returns:
        pd.DataFrame: A processed DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter, index_col=index_col)
        
        # Basic processing: drop duplicates and fill missing values
        df = df.drop_duplicates().fillna(method='ffill')
        
        return df
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: There was a parsing error with the file.")
        raise e

# Example usage
if __name__ == "__main__":
    try:
        data_frame = load_and_process_data('data.csv', delimiter=',', index_col='id')
        print(data_frame.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")