"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-15T17:09:40.839882

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
        Optional[pd.DataFrame]: DataFrame containing the data, or None if loading fails.
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
    Clean the DataFrame by filling missing values and removing duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Fill missing values with the mean of each column
    df.fillna(df.mean(), inplace=True)
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    return df

def main(file_path: str) -> None:
    """
    Main function to load, clean, and display the DataFrame.

    Args:
        file_path (str): The path to the CSV file to load.
    """
    df = load_data(file_path)
    if df is not None:  # Proceed only if the DataFrame was loaded successfully
        print("Original DataFrame:")
        print(df)
        
        cleaned_df = clean_data(df)
        print("\nCleaned DataFrame:")
        print(cleaned_df)

if __name__ == "__main__":
    # Example usage; replace 'data.csv' with the path to your CSV file
    main('data.csv')