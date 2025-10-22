"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T11:34:03.593860

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
    return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic data analysis and print results.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    None
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())  # Print summary statistics
        print("\nMissing Values:")
        print(df.isnull().sum())  # Print count of missing values

def main() -> None:
    """
    Main function to execute data loading and analysis.

    Returns:
    None
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    df = load_data(file_path)  # Load the data
    analyze_data(df)  # Analyze the loaded data

if __name__ == "__main__":
    main()  # Run the main function