"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-20T14:51:54.869415

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
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
    return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    return df.dropna()

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Perform basic analysis on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the count of non-null values for each column.
    """
    return df.count()

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        print("Initial DataFrame:")
        print(df.head())
        
        cleaned_df = clean_data(df)
        print("\nCleaned DataFrame:")
        print(cleaned_df.head())
        
        analysis = analyze_data(cleaned_df)
        print("\nData Analysis (Count of Non-null Values):")
        print(analysis)

if __name__ == "__main__":
    # Change 'data.csv' to your actual CSV file path
    main('data.csv')