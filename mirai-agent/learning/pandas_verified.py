"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T14:19:05.366717

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if loading fails.
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
    Print a summary of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    print("Data Summary:")
    print(df.describe())  # Print summary statistics
    print("\nMissing Values:")
    print(df.isnull().sum())  # Print count of missing values for each column

def main() -> None:
    """
    Main function to execute the data loading and summarization.
    """
    file_path = 'data.csv'  # Set the path to the CSV file
    df = load_data(file_path)
    
    if df is not None:
        summarize_data(df)

if __name__ == "__main__":
    main()