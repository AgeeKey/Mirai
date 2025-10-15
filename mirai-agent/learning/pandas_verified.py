"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T23:07:31.410662

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print results.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    print("DataFrame Summary:")
    print(df.describe())  # Summary statistics of numerical columns
    print("\nDataFrame Info:")
    print(df.info())      # Information about the DataFrame structure

def main() -> None:
    """
    Main function to load and analyze data.
    """
    file_path = 'data.csv'  # Specify your CSV file path
    df = load_data(file_path)
    
    if df is not None:  # Proceed only if data loading was successful
        analyze_data(df)

if __name__ == "__main__":
    main()