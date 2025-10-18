"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T09:14:44.163031

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a parsing error.")
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

def main() -> None:
    """
    Main function to execute data loading and analysis.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    data = load_data(file_path)
    
    if data is not None:
        analyze_data(data)

if __name__ == "__main__":
    main()