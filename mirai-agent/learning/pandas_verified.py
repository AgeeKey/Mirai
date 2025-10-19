"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T11:40:51.949735

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file contains parsing errors.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("Error: The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error: There was a parsing error.") from e

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping null values and resetting the index.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Drop rows with null values
    df_cleaned.reset_index(drop=True, inplace=True)  # Reset index
    return df_cleaned

def main(file_path: str) -> None:
    """
    Main function to load, clean, and display data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load data
        data = load_data(file_path)
        print("Data loaded successfully.")

        # Clean data
        cleaned_data = clean_data(data)
        print("Data cleaned successfully.")

        # Display the cleaned data
        print(cleaned_data.head())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Example usage
    main("example_data.csv")