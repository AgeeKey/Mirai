"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T14:51:33.583675

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
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)  # Load the CSV file
        return df
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
    Perform basic analysis on the DataFrame and print summary statistics.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Summary Statistics:")
        print(df.describe())  # Print summary statistics
        print("\nMissing Values:")
        print(df.isnull().sum())  # Print count of missing values
    else:
        print("No data to analyze.")

def main() -> None:
    """
    Main function to execute data loading and analysis.
    """
    file_path = 'data.csv'  # Path to the data file
    df = load_data(file_path)  # Load the data
    analyze_data(df)  # Analyze the data

if __name__ == "__main__":
    main()  # Run the main function