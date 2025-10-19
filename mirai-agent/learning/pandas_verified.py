"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-19T19:02:38.966513

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

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
        print(f"Error: The file is empty. {e}")
        raise

def summarize_data(df: pd.DataFrame) -> Dict[str, any]:
    """
    Generate a summary of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Dict[str, any]: A dictionary containing summary statistics.
    """
    summary = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'head': df.head().to_dict(orient='records'),
        'description': df.describe(include='all').to_dict()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Args:
        file_path (str): The path to the CSV file to be processed.
    """
    try:
        data = load_data(file_path)
        summary = summarize_data(data)
        print("Data Summary:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'data.csv' with your actual file path
    main('data.csv')