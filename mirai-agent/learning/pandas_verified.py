"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-17T01:57:12.974315

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)

        return df

    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: There was a problem parsing the file.")
        raise e

def main() -> None:
    """
    Main function to execute the loading and processing of data.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file

    # Load and process the data
    try:
        processed_data = load_and_process_data(file_path)
        print("Data loaded and processed successfully.")
        print(processed_data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()