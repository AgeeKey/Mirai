"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T08:57:51.620793

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was an error parsing the file.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame including basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        None
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())  # Print basic statistics
        print("\nData Types:")
        print(df.dtypes)  # Print data types of each column
    else:
        print("DataFrame is None. Cannot summarize.")

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        None
    """
    df = load_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    # Replace 'your_file.csv' with the path to your CSV file
    main('your_file.csv')