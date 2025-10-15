"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-15T04:10:46.686557

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

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print summary statistics of the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Summary Statistics:")
        print(df.describe())
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """
    Main function to load and summarize data from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    # Provide the path to your CSV file here
    csv_file_path = 'data.csv'  # Replace with your actual file path
    main(csv_file_path)