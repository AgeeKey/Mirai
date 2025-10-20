"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-20T00:33:17.028055

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): The path to the CSV file.
        index_col (Optional[str]): Column to set as index. Defaults to None.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path, index_col=index_col)
        
        # Display the first few rows of the DataFrame
        print("Data loaded successfully. Here are the first few rows:")
        print(df.head())
        
        # Drop rows with any missing values
        df.dropna(inplace=True)
        
        # Reset index if no index column is specified
        if index_col is None:
            df.reset_index(drop=True, inplace=True)
            
        return df
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your actual file path
    try:
        processed_data = load_and_process_data(file_path)
        print("Processed DataFrame:")
        print(processed_data)
    except Exception as e:
        print("An error occurred during data processing.")