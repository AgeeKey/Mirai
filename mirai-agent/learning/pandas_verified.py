"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-18T11:04:53.596016

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
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Analyze the given DataFrame by providing descriptive statistics and checking for missing values.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    None
    """
    if df is not None:
        print("Descriptive Statistics:")
        print(df.describe())  # Show basic statistics of the DataFrame
        print("\nMissing Values:")
        print(df.isnull().sum())  # Show the count of missing values for each column
    else:
        print("No data to analyze.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    None
    """
    df = load_data(file_path)  # Load the data
    analyze_data(df)  # Analyze the loaded data

if __name__ == "__main__":
    # Example usage; replace 'example.csv' with the path to your CSV file
    main('example.csv')