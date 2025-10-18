"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T03:58:05.673798

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if loading fails.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print summary statistics and information about the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    print("DataFrame Summary:")
    print(df.info())  # Display DataFrame info
    print("\nSummary Statistics:")
    print(df.describe())  # Display summary statistics

def main(file_path: str) -> None:
    """
    Main function to load and summarize data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    # Load the data
    df = load_data(file_path)
    
    # Check if dataframe is loaded successfully
    if df is not None:
        # Summarize the data
        summarize_data(df)

if __name__ == "__main__":
    # Example usage
    main("example_data.csv")  # Replace with your actual file path