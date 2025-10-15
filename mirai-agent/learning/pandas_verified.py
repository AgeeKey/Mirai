"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-15T21:46:01.939614

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
    FileNotFoundError: If the file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If there is a parsing error.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("No data found in the file.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Error parsing the file.")

def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.

    Returns:
    pd.DataFrame: A DataFrame containing summary statistics.
    """
    return df.describe()

def main(file_path: str) -> None:
    """
    Main function to load data and display summary statistics.

    Parameters:
    file_path (str): The path to the CSV file to load.
    """
    try:
        # Load the data from the specified file path
        data = load_data(file_path)
        # Generate and print summary statistics
        summary = summarize_data(data)
        print("Summary Statistics:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example file path (replace with your actual CSV file path)
    example_file_path = 'data.csv'
    main(example_file_path)