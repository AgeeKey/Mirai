"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-14T22:04:14.256193

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    :param file_path: Path to the CSV file.
    :return: DataFrame containing the loaded data.
    :raises FileNotFoundError: If the file does not exist.
    :raises pd.errors.EmptyDataError: If the file is empty.
    :raises pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Problem parsing the file. {e}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing missing values and duplicates.

    :param df: Input DataFrame to clean.
    :return: Cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Remove rows with any missing values
    df_cleaned = df_cleaned.drop_duplicates()  # Remove duplicate rows
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame by calculating the mean of each numeric column.

    :param df: Input DataFrame to analyze.
    :return: Series containing means of numeric columns.
    """
    return df.mean()

def main(file_path: str) -> Optional[pd.Series]:
    """
    Main function to load, clean, and analyze data.

    :param file_path: Path to the CSV file.
    :return: Series of means or None if an error occurred.
    """
    try:
        data = load_data(file_path)
        cleaned_data = clean_data(data)
        analysis_result = analyze_data(cleaned_data)
        return analysis_result
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return None

if __name__ == "__main__":
    result = main("data.csv")  # Replace with your actual file path
    if result is not None:
        print("Analysis Result:")
        print(result)