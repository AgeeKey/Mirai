"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-14T14:59:02.827695

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the loaded data or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was an error parsing the file.")
    return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is None or df.empty:
        print("DataFrame is empty or None. Cannot perform analysis.")
        return

    # Display basic information about the DataFrame
    print("DataFrame Information:")
    print(df.info())
    
    # Display the first five rows of the DataFrame
    print("\nFirst 5 rows of the DataFrame:")
    print(df.head())

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Parameters:
    file_path (str): The path to the CSV file to load.
    """
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    # Change 'your_file.csv' to the actual path of your CSV file
    main('your_file.csv')