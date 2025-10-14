"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-14T22:36:32.940879

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    
    Raises:
        FileNotFoundError: If the file at file_path does not exist.
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

def summarize_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Generate a summary of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Dict[str, float]: A dictionary containing summary statistics.
    """
    return {
        'mean': df.mean(numeric_only=True).to_dict(),
        'std': df.std(numeric_only=True).to_dict(),
        'count': df.count().to_dict()
    }

def main(file_path: str) -> None:
    """
    Main function to load data and print a summary.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        df = load_data(file_path)  # Load the data
        summary = summarize_data(df)  # Generate summary
        print("Summary Statistics:", summary)  # Print summary
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    # Replace 'your_file.csv' with your actual CSV file path
    main('your_file.csv')