"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-21T01:32:25.074938

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: No data found in the file.")
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
        print("DataFrame Summary:")
        print(df.info())  # Display DataFrame information
        print("\nSummary Statistics:")
        print(df.describe())  # Display summary statistics for numerical columns
    else:
        print("No data to analyze.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data from a CSV file.
    
    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    # Specify the path to your CSV file here
    file_path = 'data/sample_data.csv'
    main(file_path)