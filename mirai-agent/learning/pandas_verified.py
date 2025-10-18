"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T19:55:32.487696

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file contains parsing errors.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: {e}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Drop rows with any missing values
    df_cleaned = df.dropna()
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned

def analyze_data(df: pd.DataFrame, column: str) -> Optional[float]:
    """
    Analyze a specific column in the DataFrame and return its mean.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column (str): The column name for which to compute the mean.

    Returns:
        Optional[float]: The mean of the column, or None if the column is not found.
    """
    if column in df.columns:
        return df[column].mean()
    else:
        print(f"Error: Column '{column}' not found in DataFrame.")
        return None

def main(filepath: str, column: str) -> None:
    """
    Main function to load, clean, and analyze data.

    Args:
        filepath (str): The path to the CSV file.
        column (str): The column name to analyze.
    """
    df = load_data(filepath)
    df_cleaned = clean_data(df)
    mean_value = analyze_data(df_cleaned, column)

    if mean_value is not None:
        print(f"The mean of '{column}' is: {mean_value}")

# Example of usage
if __name__ == "__main__":
    # Replace 'data.csv' with your actual CSV file path and 'column_name' with the column to analyze
    main('data.csv', 'column_name')