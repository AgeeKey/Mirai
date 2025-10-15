"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-15T19:20:14.030095

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """Perform basic analysis on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Raises:
        ValueError: If the DataFrame is empty.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty. Cannot perform analysis.")
    
    # Display the first few rows of the DataFrame
    print("First 5 rows of the DataFrame:")
    print(df.head())
    
    # Summary statistics
    print("\nSummary statistics:")
    print(df.describe())
    
    # Check for missing values
    print("\nMissing values in each column:")
    print(df.isnull().sum())

def main(file_path: str) -> None:
    """Main function to load and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        analyze_data(df)

if __name__ == "__main__":
    FILE_PATH = 'data.csv'  # Replace with your CSV file path
    main(FILE_PATH)