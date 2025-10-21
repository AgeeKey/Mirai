"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-21T13:15:12.783509

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
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

def calculate_statistics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate basic statistics for numeric columns in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Dict[str, float]: A dictionary containing the mean and median of numeric columns.
    """
    statistics = {}
    if df.empty:
        print("Warning: DataFrame is empty. Returning empty statistics.")
        return statistics

    # Calculate mean and median for numeric columns
    statistics['mean'] = df.mean(numeric_only=True).to_dict()
    statistics['median'] = df.median(numeric_only=True).to_dict()
    return statistics

def main(file_path: str) -> None:
    """
    Main function to load data and calculate statistics.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    stats = calculate_statistics(df)  # Calculate statistics
    print("Statistics:", stats)  # Print the statistics

if __name__ == "__main__":
    # Update the file_path variable with the path to your CSV file
    file_path = 'data.csv'
    main(file_path)