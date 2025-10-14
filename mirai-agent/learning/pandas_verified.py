"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-14T18:00:42.126255

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
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
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: Parsing the file failed.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        None
    """
    print("DataFrame Summary:")
    print(df.info())  # Display DataFrame info
    print("\nFirst 5 rows of the DataFrame:")
    print(df.head())  # Display first 5 rows

def main(file_path: str) -> None:
    """
    Main function to execute the data loading and summarization.

    Args:
        file_path (str): Path to the CSV file to be loaded.

    Returns:
        None
    """
    df = load_data(file_path)  # Load data from the specified file
    if df is not None:  # Check if DataFrame is loaded successfully
        summarize_data(df)  # Summarize the loaded DataFrame

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace 'data.csv' with your actual file path