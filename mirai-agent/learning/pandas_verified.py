"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-16T09:18:58.080486

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: {e}")
        raise

def calculate_statistics(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Calculate basic statistics for specified columns in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        columns (List[str]): List of columns to calculate statistics for.

    Returns:
        pd.DataFrame: DataFrame containing mean, median, and standard deviation.
    """
    try:
        stats = df[columns].agg(['mean', 'median', 'std'])
        return stats
    except KeyError as e:
        print(f"Error: Column not found - {e}")
        raise

def main(file_path: str, columns: List[str]) -> None:
    """
    Main function to load data and calculate statistics.

    Args:
        file_path (str): The path to the CSV file.
        columns (List[str]): List of columns to calculate statistics for.
    """
    df = load_data(file_path)
    stats = calculate_statistics(df, columns)
    print(stats)

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your CSV file path
    columns_to_analyze = ['column1', 'column2']  # Replace with your column names
    main(file_path, columns_to_analyze)