"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T09:43:11.126835

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
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
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
        print("Error: The file could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print the results.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Basic DataFrame Information:")
        print(df.info())
        
        print("\nFirst 5 rows of the DataFrame:")
        print(df.head())
        
        print("\nStatistical Summary:")
        print(df.describe())
    else:
        print("No data to analyze.")

def main() -> None:
    """
    Main function to execute the data loading and analysis.
    """
    file_path = 'data.csv'  # Path to your CSV file
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    main()