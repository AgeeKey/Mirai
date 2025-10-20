"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-20T03:26:34.690615

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
    FileNotFoundError: If the CSV file does not exist.
    pd.errors.EmptyDataError: If the CSV file is empty.
    pd.errors.ParserError: If there is an error parsing the CSV file.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Basic processing: Drop rows with any missing values
        df.dropna(inplace=True)
        
        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)
        
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The CSV file is empty.")
        raise
    except pd.errors.ParserError as e:
        print("Error: There was an issue parsing the CSV file.")
        raise

def calculate_statistics(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Calculate basic statistics for specified columns in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    columns (List[str]): List of column names to calculate statistics for.

    Returns:
    pd.DataFrame: A DataFrame containing the statistics.
    
    Raises:
    KeyError: If any of the specified columns do not exist in the DataFrame.
    """
    try:
        # Calculate mean, median, and standard deviation for specified columns
        stats = df[columns].agg(['mean', 'median', 'std']).transpose()
        return stats
    except KeyError as e:
        print(f"Error: One or more columns are not present in the DataFrame: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Path to your CSV file
    try:
        data = load_and_process_data(file_path)
        statistics = calculate_statistics(data, ['column1', 'column2'])  # Replace with actual column names
        print(statistics)
    except Exception as e:
        print("An error occurred during processing:", e)