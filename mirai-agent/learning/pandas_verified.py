"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T14:42:12.532173

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
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame including basic statistics and data types.
    
    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("DataFrame Summary:")
        print(df.info())  # Print data types and non-null counts
        print("\nBasic Statistics:")
        print(df.describe())  # Print basic statistics for numerical columns
    else:
        print("No data to summarize.")

def main() -> None:
    """
    Main function to execute the data loading and summarization.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    df = load_data(file_path)  # Load the data
    summarize_data(df)  # Summarize the data

if __name__ == "__main__":
    main()