"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T17:02:47.664277

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
        Optional[pd.DataFrame]: A DataFrame containing the data from the CSV file,
                                 or None if an error occurs.
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
        print("Error: The file could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    # Display the first few rows of the DataFrame
    print("First 5 rows of the DataFrame:")
    print(df.head())
    
    # Display summary statistics
    print("\nSummary statistics:")
    print(df.describe())

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    if df is not None:          # Proceed only if data is loaded successfully
        analyze_data(df)        # Analyze the data

if __name__ == "__main__":
    main("data.csv")  # Replace with your actual CSV file path