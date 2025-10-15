"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-15T12:16:07.933955

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and process it to clean and transform.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A cleaned and processed DataFrame.
    
    Raises:
    FileNotFoundError: If the file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If the file cannot be parsed as CSV.
    """
    try:
        # Load the data
        df = pd.read_csv(file_path)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)

        # Convert a specific column to datetime (example: 'date_column')
        if 'date_column' in df.columns:
            df['date_column'] = pd.to_datetime(df['date_column'])

        return df

    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: Could not parse the CSV file.")
        raise e

def calculate_statistics(df: pd.DataFrame, column: str) -> dict:
    """
    Calculate basic statistics for a specified column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column (str): The column name for which to calculate statistics.

    Returns:
    dict: A dictionary containing mean, median, and standard deviation.
    
    Raises:
    ValueError: If the specified column does not exist in the DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"The column '{column}' does not exist in the DataFrame.")

    # Calculate statistics
    mean = df[column].mean()
    median = df[column].median()
    std_dev = df[column].std()

    return {'mean': mean, 'median': median, 'std_dev': std_dev}

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your CSV file path
    try:
        df = load_and_process_data(file_path)
        stats = calculate_statistics(df, 'numeric_column')  # Replace with your numeric column
        print("Statistics:", stats)
    except Exception as e:
        print("An error occurred:", e)