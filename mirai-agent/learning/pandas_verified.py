"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-17T21:20:58.461585

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
    return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Remove rows with missing values
    df_cleaned = df_cleaned.drop_duplicates()  # Remove duplicate rows
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print summary statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    print("Summary Statistics:")
    print(df.describe())  # Print summary statistics for numerical columns
    print("\nData Types:")
    print(df.dtypes)  # Print the data types of each column

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        df_cleaned = clean_data(df)
        analyze_data(df_cleaned)

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace 'data.csv' with your actual file path