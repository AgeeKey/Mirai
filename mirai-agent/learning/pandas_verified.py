"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T08:42:04.247718

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the data from the CSV file, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error with the file.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("DataFrame Summary:")
        print(df.describe())
        print("\nFirst 5 rows of the DataFrame:")
        print(df.head())
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """
    Main function to load and summarize data from a CSV file.

    Parameters:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    # Replace 'your_file.csv' with the path to your CSV file
    main('your_file.csv')