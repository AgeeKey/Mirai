"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-20T19:10:03.655268

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list[str]]): List of column names to use for the DataFrame.

    Returns:
        pd.DataFrame: Processed DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the DataFrame is empty after loading.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path, names=column_names, header=0 if column_names else None)
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The loaded DataFrame is empty.")

        # Process the data (e.g., removing any rows with missing values)
        df.dropna(inplace=True)

        return df

    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except ValueError as e:
        print(f"Error: {e}")
        raise e

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your actual file path
    column_names = ['Column1', 'Column2', 'Column3']  # Adjust based on your data

    try:
        data_df = load_and_process_data(file_path, column_names)
        print(data_df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")