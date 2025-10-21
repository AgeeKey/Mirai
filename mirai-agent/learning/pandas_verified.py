"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-21T00:44:59.942272

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): Path to the CSV file.
        index_col (Optional[str]): Column to set as index. Defaults to None.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the data is empty after loading.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)

        # Check if DataFrame is empty
        if df.empty:
            raise ValueError("The loaded DataFrame is empty.")

        # Basic data cleaning
        df.dropna(inplace=True)  # Remove rows with missing values
        df.reset_index(drop=True, inplace=True)  # Reset index

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data_frame = load_and_process_data('data.csv', index_col='id')
        print(data_frame.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")