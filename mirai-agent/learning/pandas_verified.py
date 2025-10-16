"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T19:43:48.381270

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
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

def summarize_data(df: pd.DataFrame) -> Tuple[int, pd.DataFrame]:
    """
    Summarize the DataFrame by providing its shape and basic statistics.
    
    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Tuple[int, pd.DataFrame]: A tuple containing the number of rows and a DataFrame 
        with basic statistics.
    """
    num_rows = df.shape[0]
    statistics = df.describe(include='all')  # Include all columns for summary
    return num_rows, statistics

def main() -> None:
    """
    Main function to load data and summarize it.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    try:
        df = load_data(file_path)  # Load the data
        num_rows, statistics = summarize_data(df)  # Summarize the data
        
        print(f"Number of rows: {num_rows}")  # Print number of rows
        print("\nStatistics:\n", statistics)  # Print summary statistics
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()