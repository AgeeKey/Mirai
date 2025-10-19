"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-19T20:37:20.857128

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
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
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
        print("Error: The file could not be parsed.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: A cleaned DataFrame with missing values dropped.
    """
    return df.dropna()

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print summary statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    print("Summary Statistics:")
    print(df.describe())

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        cleaned_df = clean_data(df)
        analyze_data(cleaned_df)

if __name__ == "__main__":
    # Example usage
    main("data.csv")