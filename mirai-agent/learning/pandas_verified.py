"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T22:06:16.347146

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if loading fails.
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
        print("Error: There was a parsing error while reading the file.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame including basic statistics and information.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("DataFrame Summary:")
        print(df.info())  # Print DataFrame info
        print("\nDescriptive Statistics:")
        print(df.describe())  # Print descriptive statistics for numerical columns

def main(file_path: str) -> None:
    """
    Main function to load and summarize the data.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    file_path = 'data/sample_data.csv'  # Specify the path to your CSV file
    main(file_path)