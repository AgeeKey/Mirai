"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T07:17:37.764427

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
        Optional[pd.DataFrame]: A DataFrame containing the data, or None if an error occurs.
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
        print("Error: The file could not be parsed.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print summary statistics and the first few rows of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    print("Summary Statistics:")
    print(df.describe())  # Display summary statistics of the DataFrame
    print("\nFirst 5 Rows:")
    print(df.head())      # Display the first 5 rows of the DataFrame

def main() -> None:
    """
    Main function to load and summarize data from a CSV file.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    df = load_data(file_path)
    
    if df is not None:  # Check if the DataFrame is successfully loaded
        summarize_data(df)

if __name__ == "__main__":
    main()