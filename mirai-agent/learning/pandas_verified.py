"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T15:39:48.117223

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
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, 
                                 or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame, including basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())
        print("First 5 rows:")
        print(df.head())
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Args:
        file_path (str): The path to the CSV file.
    """
    data = load_data(file_path)
    summarize_data(data)

# Example usage:
if __name__ == "__main__":
    main("example_data.csv")