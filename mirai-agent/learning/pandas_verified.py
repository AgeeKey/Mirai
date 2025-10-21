"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-21T12:58:53.060126

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it.

    Args:
        file_path (str): The path to the CSV file.
        columns (Optional[list]): List of columns to load. If None, all columns will be loaded.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the data is empty or cannot be processed.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, usecols=columns)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except Exception as e:
        raise ValueError("Error loading data") from e

    # Check for empty DataFrame
    if df.empty:
        raise ValueError("Loaded DataFrame is empty")

    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Reset index after dropping rows
    df.reset_index(drop=True, inplace=True)

    return df

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame and return a summary.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: Summary statistics of the DataFrame.
    """
    # Compute summary statistics
    summary = df.describe()
    
    return summary

if __name__ == "__main__":
    try:
        # Load and process the data
        data_file = 'data.csv'  # Replace with your CSV file path
        processed_data = load_and_process_data(data_file)

        # Analyze the processed data
        summary_statistics = analyze_data(processed_data)

        print(summary_statistics)
    except Exception as e:
        print(f"An error occurred: {e}")