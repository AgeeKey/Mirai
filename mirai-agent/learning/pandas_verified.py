"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-16T21:53:28.072436

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by removing missing values.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
    FileNotFoundError: If the specified file path does not exist.
    pd.errors.EmptyDataError: If the CSV file is empty.
    pd.errors.ParserError: If there is a parsing error in the CSV file.
    """
    try:
        # Load data into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: {e}")
        raise

    # Remove rows with any missing values
    df_cleaned = df.dropna()

    return df_cleaned

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print the summary statistics and information of the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    # Print summary statistics
    print(df.describe())

    # Print information about the DataFrame
    print(df.info())

def main(file_path: str) -> None:
    """
    Main function to load, process, and summarize the data.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_and_process_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    # Example CSV file path (replace with your actual file path)
    csv_file_path = 'data.csv'
    main(csv_file_path)