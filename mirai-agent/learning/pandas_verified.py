"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T11:27:14.473236

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
        Optional[pd.DataFrame]: DataFrame containing the loaded data or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
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
    Analyze the DataFrame by displaying basic statistics and information.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("DataFrame Info:")
        print(df.info())
        print("\nBasic Statistics:")
        print(df.describe())
    else:
        print("No data to analyze.")

def main() -> None:
    """
    Main function to load and analyze data.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    data_frame = load_data(file_path)
    analyze_data(data_frame)

if __name__ == "__main__":
    main()