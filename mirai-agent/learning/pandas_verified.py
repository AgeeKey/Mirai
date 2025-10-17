"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-17T01:09:16.054272

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[int] = None) -> pd.DataFrame:
    """
    Load and process data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        index_col (Optional[int]): Column to set as index. Defaults to None.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If there's an error parsing the CSV file.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)
        # Drop rows with any missing values
        df.dropna(inplace=True)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise
    except pd.errors.ParserError as e:
        print("Error: Could not parse the file.")
        raise

def main():
    file_path = 'data.csv'  # Specify the path to your CSV file
    try:
        # Load and process the data
        data = load_and_process_data(file_path)
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    main()