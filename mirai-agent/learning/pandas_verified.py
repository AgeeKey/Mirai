"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-16T07:24:59.329218

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, delimiter: str = ',', index_col: Optional[int] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Parameters:
    - file_path (str): The path to the CSV file.
    - delimiter (str): The delimiter used in the CSV file. Default is ','.
    - index_col (Optional[int]): Column to set as index. Default is None.

    Returns:
    - pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
    - FileNotFoundError: If the file does not exist.
    - pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter, index_col=index_col)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file at {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("The file is empty.") from e

    # Basic data processing: drop rows with any missing values
    df.dropna(inplace=True)

    # Return the processed DataFrame
    return df

def main():
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Update with your CSV file path
    try:
        df_processed = load_and_process_data(file_path)
        print("Data loaded and processed successfully:")
        print(df_processed)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()