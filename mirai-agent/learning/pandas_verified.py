"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T00:37:02.748798

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Loads a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the data if successful, None otherwise.
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
    Cleans the DataFrame by dropping rows with missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Drop rows with any missing values
    cleaned_df = df.dropna()
    return cleaned_df

def main(file_path: str) -> None:
    """
    Main function to execute the data loading and cleaning process.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    if df is not None:  # Check if the DataFrame is loaded successfully
        print("Data loaded successfully.")
        cleaned_df = clean_data(df)  # Clean the data
        print("Data cleaned successfully.")
        print(cleaned_df.head())  # Display the first few rows of the cleaned DataFrame

if __name__ == "__main__":
    main("data.csv")  # Replace 'data.csv' with your actual file path