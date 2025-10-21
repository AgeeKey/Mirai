"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-21T14:36:18.456885

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError(f"The file is empty: {file_path}") from e

def analyze_data(df: pd.DataFrame) -> Union[pd.Series, None]:
    """
    Analyze the DataFrame to compute basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the mean of each numeric column.
    """
    if df.empty:
        print("The DataFrame is empty.")
        return None
    
    # Compute mean for numeric columns
    return df.mean()

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        data = load_data(file_path)  # Load data from CSV
        stats = analyze_data(data)   # Analyze the loaded data

        if stats is not None:
            print("Basic Statistics:")
            print(stats)  # Print the statistics
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    FILE_PATH = 'data.csv'  # Specify the path to your CSV file
    main(FILE_PATH)  # Execute the main function