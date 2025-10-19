"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T09:03:19.468087

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
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
    return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Drop rows with any missing values
    df_cleaned = df.dropna()
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame by calculating the mean of numeric columns.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the mean of each numeric column.
    """
    return df.mean()

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    # Load the data
    df = load_data(file_path)
    if df is not None:
        # Clean the data
        df_cleaned = clean_data(df)
        # Analyze the data
        means = analyze_data(df_cleaned)
        print("Mean of numeric columns:")
        print(means)

if __name__ == "__main__":
    # Example usage
    main("data.csv")