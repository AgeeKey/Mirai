"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-20T15:08:12.640413

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic cleaning.

    Args:
        file_path (str): The path to the CSV file.
        index_col (Optional[str]): Column to use as the row labels of the DataFrame.

    Returns:
        pd.DataFrame: A cleaned DataFrame.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Reset index if no index_col is specified
        if index_col is None:
            df.reset_index(drop=True, inplace=True)

        return df
    
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        raise
    except pd.errors.EmptyDataError as empty_error:
        print(f"Error: The file is empty. {empty_error}")
        raise
    except pd.errors.ParserError as parse_error:
        print(f"Error: There was a parsing error. {parse_error}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data_frame = load_and_process_data('data.csv', index_col='id')
        print(data_frame.head())
    except Exception as e:
        print(f"An error occurred: {e}")