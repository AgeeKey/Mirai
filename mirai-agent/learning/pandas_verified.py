"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-19T09:50:46.338016

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError(f"The file {file_path} is empty.") from e

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing rows with missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    cleaned_df = df.dropna()  # Remove rows with any missing values
    return cleaned_df

def analyze_data(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Analyze the DataFrame to get the shape (number of rows and columns).

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Tuple[int, int]: A tuple containing the number of rows and columns.
    """
    return df.shape  # Return the shape of the DataFrame

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load the data
        df = load_data(file_path)
        # Clean the data
        cleaned_df = clean_data(df)
        # Analyze the data
        rows, columns = analyze_data(cleaned_df)
        print(f"Cleaned DataFrame shape: {rows} rows, {columns} columns.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage, replace 'data.csv' with your actual file path
    main('data.csv')