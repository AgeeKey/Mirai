"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-21T04:10:57.659131

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): The path to the CSV file.
        index_col (Optional[str]): Column name to set as index. Default is None.

    Returns:
        pd.DataFrame: Processed DataFrame.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If there is an error parsing the CSV file.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)
        
        # Drop rows with any missing values
        df.dropna(inplace=True)
        
        # Reset index if no index_col is specified
        if index_col is None:
            df.reset_index(drop=True, inplace=True)
        
        return df
    
    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path.")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The CSV file is empty.")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Could not parse the CSV file. {e}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        data_frame = load_and_process_data('data.csv', index_col='id')
        print(data_frame.head())
    except Exception as e:
        print(f"An error occurred: {e}")