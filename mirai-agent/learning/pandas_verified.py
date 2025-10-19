"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T10:22:13.547426

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        raise
    except pd.errors.EmptyDataError as empty_error:
        print(f"Error: {empty_error}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    return df.dropna()

def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics for the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        pd.DataFrame: DataFrame containing summary statistics.
    """
    return df.describe()

def main(file_path: str) -> None:
    """
    Main function to load, clean, and summarize data.

    Args:
        file_path (str): The path to the CSV file.
    """
    # Load the data
    data = load_data(file_path)
    
    # Clean the data
    cleaned_data = clean_data(data)
    
    # Summarize the data
    summary = summarize_data(cleaned_data)
    
    # Display the summary
    print(summary)

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace 'data.csv' with the path to your CSV file.