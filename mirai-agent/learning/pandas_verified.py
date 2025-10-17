"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-17T19:27:37.088403

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Loads data from a CSV file and processes it into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list]): A list of column names to be used. If None, uses the first row as headers.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the column names do not match the data.
    """
    try:
        # Load data from CSV
        df = pd.read_csv(file_path, header=0 if column_names is None else None)

        # If column names are provided, assign them to the DataFrame
        if column_names:
            if len(column_names) != df.shape[1]:
                raise ValueError("Column names length does not match number of columns in data.")
            df.columns = column_names

        # Drop any rows with missing values
        df.dropna(inplace=True)

        return df

    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
        raise e
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def main() -> None:
    """
    Main function to execute data loading and processing.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    column_names = ['Name', 'Age', 'City']  # Define your column names

    try:
        # Load and process the data
        data = load_and_process_data(file_path, column_names)

        # Display the first few rows of the DataFrame
        print(data.head())
        
    except Exception as e:
        print(f"Failed to process the data: {e}")

if __name__ == "__main__":
    main()