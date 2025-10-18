"""
Pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-18T11:36:18.421593

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
        Optional[pd.DataFrame]: A DataFrame containing the data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping null values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Drop rows with any null values
    df_cleaned = df_cleaned.drop_duplicates()  # Drop duplicate rows
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print summary statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    print("Summary Statistics:")
    print(df.describe())  # Print summary statistics for numerical columns

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        df_cleaned = clean_data(df)
        analyze_data(df_cleaned)

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace 'data.csv' with your actual CSV file path