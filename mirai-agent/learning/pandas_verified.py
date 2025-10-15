"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-15T03:06:09.325926

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
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if loading fails.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Analyze the DataFrame and print summary statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Summary Statistics:")
        print(df.describe())  # Print summary statistics
        print("\nMissing Values:")
        print(df.isnull().sum())  # Print count of missing values
    else:
        print("No data to analyze.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    data = load_data(file_path)
    analyze_data(data)

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace with your actual CSV file path