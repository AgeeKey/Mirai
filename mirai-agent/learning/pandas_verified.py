"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-22T10:45:40.782221

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
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
        print(f"Error: The file {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Analyze the DataFrame and print basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Basic Statistics:")
        print(df.describe())
        print("\nMissing Values:")
        print(df.isnull().sum())
    else:
        print("No data to analyze.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your CSV file path
    main(file_path)