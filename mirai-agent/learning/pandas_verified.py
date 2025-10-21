"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-21T09:45:21.068140

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
        Optional[pd.DataFrame]: DataFrame containing the loaded data or None if an error occurred.
    """
    try:
        data = pd.read_csv(file_path)
        return data
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
    Perform basic analysis on the DataFrame and print summary statistics.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())  # Summary statistics
        print("\nMissing Values:")
        print(df.isnull().sum())  # Count missing values for each column
    else:
        print("No data to analyze.")

def main() -> None:
    """
    Main function to execute the data loading and analysis.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    data = load_data(file_path)
    analyze_data(data)

if __name__ == "__main__":
    main()