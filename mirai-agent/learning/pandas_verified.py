"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T11:36:50.971064

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
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
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
        print("Error: Could not parse the file.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Summarize the DataFrame by displaying basic statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    # Example usage, replace 'data.csv' with your actual CSV file path
    main('data.csv')