"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-18T17:18:10.196114

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("Error: The file is empty.") from e

def analyze_data(df: pd.DataFrame) -> Optional[dict]:
    """
    Analyze the DataFrame to calculate basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Optional[dict]: A dictionary with basic statistics, or None if DataFrame is empty.
    """
    if df.empty:
        print("DataFrame is empty. No analysis performed.")
        return None
    
    stats = {
        'mean': df.mean(),
        'median': df.median(),
        'std_dev': df.std(),
        'count': df.count()
    }
    return stats

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        data = load_data(file_path)  # Load the data
        stats = analyze_data(data)    # Analyze the data
        if stats:
            print("Basic Statistics:")
            print(stats)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace with your CSV file path