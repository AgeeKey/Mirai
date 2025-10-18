"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T04:29:53.523017

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
        print("Error: There was a problem parsing the file.")
        return None

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the DataFrame by dropping missing values and normalizing numeric columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to be processed.

    Returns:
    pd.DataFrame: A processed DataFrame with missing values dropped and numeric columns normalized.
    """
    # Drop rows with any missing values
    df_cleaned = df.dropna()
    
    # Normalize numeric columns
    numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
    df_cleaned[numeric_cols] = (df_cleaned[numeric_cols] - df_cleaned[numeric_cols].mean()) / df_cleaned[numeric_cols].std()
    
    return df_cleaned

def main(file_path: str) -> None:
    """
    Main function to load, process, and display data.

    Parameters:
    file_path (str): The path to the CSV file to be processed.
    """
    df = load_data(file_path)
    if df is not None:
        df_processed = process_data(df)
        print("Processed DataFrame:")
        print(df_processed)

if __name__ == "__main__":
    # Change the file path to the location of your CSV file
    main('data.csv')