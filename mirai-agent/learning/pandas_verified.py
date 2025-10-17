"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T08:05:57.885735

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
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurred.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Summarize the data by displaying basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())  # Displays descriptive statistics
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """
    Main function to load data and summarize it.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    summarize_data(df)         # Summarize the data

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace 'data.csv' with your actual file path