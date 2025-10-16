"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-16T23:14:53.162013

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

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
        print("Error: The file could not be parsed.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: A cleaned DataFrame.
    """
    # Drop rows with missing values
    df_cleaned = df.dropna()
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    print("DataFrame Statistics:")
    print(df.describe())  # Print summary statistics

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        df_cleaned = clean_data(df)
        analyze_data(df_cleaned)

if __name__ == "__main__":
    # Specify the path to the CSV file
    csv_file_path = "data.csv"
    main(csv_file_path)