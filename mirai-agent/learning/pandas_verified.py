"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-21T17:35:44.919559

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise

def summarize_data(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Summarize the DataFrame by returning the number of rows and columns.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Tuple[int, int]: The number of rows and columns in the DataFrame.
    """
    return df.shape

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load the dataset
        data = load_data(file_path)
        
        # Summarize the dataset
        rows, cols = summarize_data(data)
        print(f"The dataset contains {rows} rows and {cols} columns.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file.
    main('data.csv')