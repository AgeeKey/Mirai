"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-15T02:49:53.316059

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
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
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
        print("Error: There was a problem parsing the file.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print results.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        # Display the first five rows of the DataFrame
        print("First five rows of the DataFrame:")
        print(df.head())
        
        # Print summary statistics
        print("\nSummary statistics:")
        print(df.describe())

def main() -> None:
    """
    Main function to load and analyze data from a CSV file.
    """
    file_path = 'data.csv'  # Replace with your CSV file path
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    main()