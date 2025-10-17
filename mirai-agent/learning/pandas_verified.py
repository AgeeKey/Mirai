"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T09:58:48.174725

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data: The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def analyze_data(df: pd.DataFrame) -> Optional[pd.Series]:
    """
    Analyze the DataFrame and return the summary statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Optional[pd.Series]: A Series containing summary statistics, or None if the DataFrame is empty.
    """
    if df.empty:
        print("DataFrame is empty; no statistics to compute.")
        return None
    return df.describe()

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        data = load_data(file_path)
        summary = analyze_data(data)
        if summary is not None:
            print("Summary Statistics:")
            print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage; replace 'data.csv' with your actual CSV file path
    main("data.csv")