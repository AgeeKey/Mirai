"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-14T15:48:30.681774

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is None or df.empty:
        print("DataFrame is empty or None, cannot perform analysis.")
        return

    # Display basic information about the DataFrame
    print("DataFrame Info:")
    print(df.info())
    
    # Display basic statistics for numerical columns
    print("\nDescriptive Statistics:")
    print(df.describe())

def main() -> None:
    """
    Main function to load and analyze data.
    """
    file_path = 'data.csv'  # Update with the path to your CSV file
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    main()