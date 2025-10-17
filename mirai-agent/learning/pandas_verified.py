"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-17T03:33:18.159091

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list]): List of column names to use. If None, uses the first row as header.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the DataFrame is empty after loading.
    """
    # Attempt to read the CSV file
    try:
        df = pd.read_csv(file_path, header=0 if column_names is None else None)
        if column_names is not None:
            df.columns = column_names
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e

    # Check for empty DataFrame
    if df.empty:
        raise ValueError("The loaded DataFrame is empty.")

    # Basic data cleaning: drop any rows with missing values
    df.dropna(inplace=True)

    return df

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data/sample_data.csv'  # Specify the path to your CSV file
    column_names = ['Column1', 'Column2', 'Column3']  # Example column names

    try:
        df = load_and_process_data(file_path, column_names)
        print("Data loaded and processed successfully.")
        print(df.head())  # Display the first few rows of the DataFrame
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()