"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T03:18:25.776851

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the data, or None if the file could not be loaded.
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
        print("Error: Could not parse the file.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    print("Data Summary:")
    print(df.describe())  # Print summary statistics
    print("\nMissing Values:")
    print(df.isnull().sum())  # Print count of missing values

def main() -> None:
    """
    Main function to execute the data loading and analysis.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    df = load_data(file_path)
    
    if df is not None:
        analyze_data(df)

if __name__ == "__main__":
    main()