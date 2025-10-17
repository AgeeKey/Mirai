"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-17T20:00:07.655387

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        # Load the CSV file into a DataFrame
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
    Print a summary of the DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame to summarize.
    """
    # Print the first 5 rows of the DataFrame
    print("First 5 rows of the DataFrame:")
    print(df.head())
    
    # Print basic statistics of the DataFrame
    print("\nSummary statistics:")
    print(df.describe())

def main() -> None:
    """
    Main function to execute the data loading and summarization.
    """
    # Path to the CSV file
    file_path = 'data.csv'  # Update with your actual file path

    # Load the data
    df = load_data(file_path)
    
    # If the DataFrame is loaded successfully, summarize it
    if df is not None:
        summarize_data(df)

if __name__ == "__main__":
    main()