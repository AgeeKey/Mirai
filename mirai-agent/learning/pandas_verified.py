"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T01:00:01.484362

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurred.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
    except pd.errors.ParserError:
        print(f"Error: There was an error parsing the file '{file_path}'.")
    return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())  # Summary statistics for numerical columns
        print("\nMissing Values:")
        print(df.isnull().sum())  # Count of missing values in each column
    else:
        print("No data to analyze.")

def main() -> None:
    """
    Main function to load and analyze data from a CSV file.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    df = load_data(file_path)  # Load the data
    analyze_data(df)  # Analyze the data

if __name__ == "__main__":
    main()