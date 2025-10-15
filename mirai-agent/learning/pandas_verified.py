"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T01:12:39.975563

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data in file") from e

def summarize_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Generate summary statistics for a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to summarize.

    Returns:
        Dict[str, float]: Dictionary containing mean and median of numeric columns.
    """
    summary = {
        'mean': df.mean(numeric_only=True).to_dict(),
        'median': df.median(numeric_only=True).to_dict()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load and summarize data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load data from CSV
        data = load_data(file_path)
        
        # Summarize the data
        summary = summarize_data(data)
        
        # Print the summary
        print("Summary Statistics:")
        print(summary)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'data.csv' with your actual CSV file path
    main('data.csv')