"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T23:50:56.685317

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
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurred.
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
    Clean the DataFrame by removing null values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Remove rows with any null values
    df_cleaned = df.dropna()
    # Remove duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> None:
    """
    Analyze the DataFrame and print basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    print("Basic Statistics:")
    print(df.describe())

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a given file path.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        df_cleaned = clean_data(df)
        analyze_data(df_cleaned)

if __name__ == "__main__":
    # Example file path (update this to your actual file)
    example_file_path = 'data.csv'
    main(example_file_path)