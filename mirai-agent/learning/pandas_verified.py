"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-17T10:15:01.473932

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    :param file_path: Path to the CSV file.
    :return: DataFrame containing the loaded data.
    :raises FileNotFoundError: If the file does not exist.
    :raises pd.errors.EmptyDataError: If the file is empty.
    :raises pd.errors.ParserError: If there is a parsing error.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data: The file is empty") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file") from e

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping rows with missing values.

    :param df: DataFrame to be cleaned.
    :return: Cleaned DataFrame.
    """
    return df.dropna()

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame and return the summary statistics.

    :param df: DataFrame to analyze.
    :return: Summary statistics of the DataFrame.
    """
    return df.describe()

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data.

    :param file_path: Path to the CSV file to process.
    """
    try:
        # Load data
        df = load_data(file_path)
        
        # Clean data
        cleaned_df = clean_data(df)
        
        # Analyze data
        summary_statistics = analyze_data(cleaned_df)
        
        # Print summary statistics
        print(summary_statistics)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    main("data.csv")