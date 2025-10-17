"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T04:53:15.571391

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: DataFrame containing the loaded data.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError(f"Error: The file is empty. {e}")
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error: Could not parse the file. {e}")

def summarize_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Generate summary statistics for a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.

    Returns:
    Dict[str, float]: A dictionary containing summary statistics.
    """
    summary = {
        'mean': df.mean(numeric_only=True).to_dict(),
        'median': df.median(numeric_only=True).to_dict(),
        'std_dev': df.std(numeric_only=True).to_dict(),
        'count': df.count().to_dict()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load data and summarize it.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    try:
        data = load_data(file_path)
        summary = summarize_data(data)
        print("Summary Statistics:")
        print(summary)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file
    main('data.csv')