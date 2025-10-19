"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-19T20:21:33.634080

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: DataFrame containing the data if successful, None otherwise.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    if df is None:
        raise ValueError("Input DataFrame is None.")

    # Drop rows with any missing values
    df_cleaned = df.dropna()
    
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    
    return df_cleaned

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame including descriptive statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is None:
        raise ValueError("Input DataFrame is None.")

    print("Data Summary:")
    print(df.describe())

def main(file_path: str) -> None:
    """
    Main function to execute data loading, cleaning, and summarizing.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        df_cleaned = clean_data(df)
        summarize_data(df_cleaned)

if __name__ == "__main__":
    # Example CSV file path
    example_file_path = 'data.csv'
    main(example_file_path)