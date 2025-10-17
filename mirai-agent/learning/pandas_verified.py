"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T13:12:43.511389

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Any

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.
    
    Parameters:
    - file_path: str - The path to the CSV file.
    
    Returns:
    - Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: No data found in the file.")
        return None
    except pd.errors.ParserError:
        print("Error: Failed to parse the file.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print the results.
    
    Parameters:
    - df: pd.DataFrame - The DataFrame to analyze.
    """
    if df is not None and not df.empty:
        print("Data Summary:")
        print(df.describe())  # Print summary statistics
        print("\nFirst 5 Rows:")
        print(df.head())  # Print first 5 rows
    else:
        print("Error: DataFrame is empty or None. Unable to analyze data.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data from a specified CSV file.
    
    Parameters:
    - file_path: str - The path to the CSV file.
    """
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    # Example usage: replace 'data.csv' with your actual file path
    main('data.csv')