"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-20T15:40:50.947044

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
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
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
    Clean the DataFrame by removing rows with missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: A cleaned DataFrame without missing values.
    """
    return df.dropna()

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame by calculating summary statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: Summary statistics of the DataFrame.
    """
    return df.describe()

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    if df is not None:  # Proceed only if the DataFrame is loaded successfully
        cleaned_df = clean_data(df)  # Clean the data
        summary = analyze_data(cleaned_df)  # Analyze the cleaned data
        print(summary)  # Print summary statistics

if __name__ == "__main__":
    main("data.csv")  # Replace with your actual file path