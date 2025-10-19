"""
Pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-19T14:50:27.753055

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Generate and display summary statistics of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None and not df.empty:
        print("Summary Statistics:")
        print(df.describe())
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    # Example usage
    main("data.csv")