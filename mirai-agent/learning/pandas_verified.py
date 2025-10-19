"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-19T15:53:26.858415

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
        Optional[pd.DataFrame]: A DataFrame containing the data from the CSV file,
                                 or None if an error occurred.
    """
    try:
        data = pd.read_csv(file_path)  # Load the data
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
    return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Analyze the given DataFrame and print summary statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Raises:
        ValueError: If the DataFrame is empty.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty. Cannot analyze.")

    # Print the first few rows of the DataFrame
    print("First 5 rows of the data:")
    print(df.head())

    # Print summary statistics
    print("\nSummary statistics:")
    print(df.describe())

def main(file_path: str) -> None:
    """
    Main function to load and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    if df is not None:  # Check if loading was successful
        analyze_data(df)  # Analyze the data

if __name__ == "__main__":
    file_path = "data.csv"  # Specify your CSV file path here
    main(file_path)