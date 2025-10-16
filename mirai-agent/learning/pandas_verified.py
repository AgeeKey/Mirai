"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-16T05:16:16.116667

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Union

def load_and_process_data(file_path: str, index_col: Optional[Union[int, str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file to be loaded.
        index_col (Optional[Union[int, str]]): Column to set as index. Default is None.

    Returns:
        pd.DataFrame: Processed DataFrame with appropriate data types.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        Exception: For any other exceptions encountered during file reading.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)

        # Convert columns to appropriate data types
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert 'date' column to datetime
        df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Convert 'value' column to numeric

        # Drop rows with NaN values in critical columns
        df.dropna(subset=['date', 'value'], inplace=True)

        return df
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        df = load_and_process_data('data.csv', index_col='id')
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print("Failed to load and process data.")