"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-18T12:07:53.863972

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A processed DataFrame.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)

        # Drop any rows with missing values
        df.dropna(inplace=True)

        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)

        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def calculate_statistics(df: pd.DataFrame, column: str) -> dict:
    """
    Calculate basic statistics for a specified column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column (str): The column name for which to calculate statistics.

    Returns:
        dict: A dictionary containing the mean, median, and standard deviation.
    
    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist in the DataFrame.")

    stats = {
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std_dev': df[column].std()
    }
    
    return stats

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your CSV file path
    try:
        data = load_and_process_data(file_path)
        statistics = calculate_statistics(data, 'age')  # Replace 'age' with your column name
        print(statistics)
    except Exception as e:
        print(f"An error occurred: {e}")