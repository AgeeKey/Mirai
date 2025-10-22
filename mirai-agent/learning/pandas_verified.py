"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 1/1
Learned: 2025-10-22T18:45:31.017585

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if loading fails.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file at {file_path} could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print summary statistics.

    Args:
        df (pd.DataFrame): DataFrame containing the data to analyze.
    """
    if df is not None and not df.empty:
        print("Data Summary:")
        print(df.describe())  # Display summary statistics
        print("\nData Types:")
        print(df.dtypes)      # Display data types
    else:
        print("No data to analyze.")

def main() -> None:
    """
    Main function to execute the data loading and analysis.
    """
    file_path = 'data.csv'  # Path to the CSV file
    df = load_data(file_path)  # Load the data
    analyze_data(df)           # Analyze the data

if __name__ == "__main__":
    main()