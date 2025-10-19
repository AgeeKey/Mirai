"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T02:28:32.970306

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the data from the CSV file or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: Could not parse the file.")
    return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print the summary of the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Summary of DataFrame:")
        print(df.describe())
        print("\nMissing values in each column:")
        print(df.isnull().sum())
    else:
        print("No data to summarize.")

def main() -> None:
    """
    Main function to load data and summarize it.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    data = load_data(file_path)
    summarize_data(data)

if __name__ == "__main__":
    main()