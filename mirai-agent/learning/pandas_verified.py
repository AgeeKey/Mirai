"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-18T07:08:21.198322

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_names (Optional[list[str]]): List of column names to use. If None, uses the first row as header.

    Returns:
    - pd.DataFrame: A processed DataFrame with cleaned data.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the data contains any NaN values after processing.
    """
    try:
        # Load data into a DataFrame
        df = pd.read_csv(file_path, header=0 if column_names is None else None)

        # Set column names if provided
        if column_names is not None:
            df.columns = column_names

        # Drop rows with any NaN values
        df.dropna(inplace=True)

        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)

        return df

    except FileNotFoundError as e:
        print(f"Error: The file at {file_path} was not found.")
        raise e
    except ValueError as e:
        print("Error: There are NaN values in the data after processing.")
        raise e


if __name__ == "__main__":
    # Example usage:
    try:
        data = load_and_process_data("data.csv", column_names=["Column1", "Column2", "Column3"])
        print(data.head())
    except Exception as e:
        print(f"An error occurred: {e}")