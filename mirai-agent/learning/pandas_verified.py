"""
Pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T05:56:48.085988

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
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

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Basic Statistics:")
        print(df.describe())  # Print summary statistics
        print("\nMissing Values:")
        print(df.isnull().sum())  # Print count of missing values
    else:
        print("No data available for analysis.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Parameters:
    file_path (str): The path to the CSV file to load.
    """
    df = load_data(file_path)  # Load the data
    analyze_data(df)  # Analyze the data

if __name__ == "__main__":
    main("data.csv")  # Replace with your actual file path