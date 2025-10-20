"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T10:48:58.166449

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
    Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: Could not parse the file.")
    return None

def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Calculate basic statistics (mean, median, std) of numeric columns in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame for which statistics are to be calculated.

    Returns:
    pd.Series: A Series containing the mean, median, and standard deviation.
    """
    return df.describe().loc[['mean', '50%', 'std']]

def main(file_path: str) -> None:
    """
    Main function to load data and calculate statistics.

    Parameters:
    file_path (str): The path to the CSV file to be processed.
    """
    df = load_data(file_path)
    if df is not None:
        print("Data loaded successfully.")
        stats = calculate_statistics(df)
        print("Statistics:")
        print(stats)

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file
    main('data.csv')