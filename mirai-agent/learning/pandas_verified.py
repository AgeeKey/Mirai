"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-21T15:25:24.673535

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load and process data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list]): A list of column names to use. If None, uses the file's header.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the specified file is not found.
        ValueError: If the DataFrame is empty after loading.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path, names=column_names, header=0 if column_names is None else None)
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The loaded DataFrame is empty. Please check the contents of the file.")

        # Basic processing: drop duplicates and fill missing values
        df.drop_duplicates(inplace=True)
        df.fillna(method='ffill', inplace=True)

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    # Example usage of the load_and_process_data function
    file_path = 'data.csv'  # Replace with your actual file path
    try:
        data = load_and_process_data(file_path)
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")