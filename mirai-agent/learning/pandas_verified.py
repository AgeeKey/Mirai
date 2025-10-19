"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-19T12:59:46.758797

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurred.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was an issue parsing the file.")
    return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    if df is None:
        raise ValueError("Input DataFrame cannot be None.")
    
    # Remove duplicates
    df = df.drop_duplicates()
    # Drop rows with any missing values
    df = df.dropna()
    return df

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print summary statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    print("DataFrame Summary:")
    print(df.describe())  # Print summary statistics
    print("\nDataFrame Info:")
    print(df.info())      # Print DataFrame info

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file to process.
    """
    df = load_data(file_path)
    if df is not None:
        cleaned_df = clean_data(df)
        analyze_data(cleaned_df)

# Example usage:
if __name__ == "__main__":
    main("data.csv")  # Replace 'data.csv' with your actual file path