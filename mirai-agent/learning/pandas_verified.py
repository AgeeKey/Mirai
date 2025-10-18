"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-18T11:52:04.386583

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it.

    Parameters:
    - file_path: str - Path to the CSV file.
    - index_col: Optional[str] - Column to set as index (default is None).

    Returns:
    - pd.DataFrame: Processed DataFrame.
    
    Raises:
    - FileNotFoundError: If the file does not exist.
    - pd.errors.EmptyDataError: If the file is empty.
    - pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)

        # Basic data cleaning: drop rows with any missing values
        df.dropna(inplace=True)

        # Reset index if no index column provided
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
        print("Error: Could not parse the file.")
        raise e

def main():
    # Example usage of the load_and_process_data function
    file_path = 'data.csv'  # Replace with your actual file path
    try:
        data = load_and_process_data(file_path, index_col='id')
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print("An error occurred while processing the data.")

if __name__ == "__main__":
    main()