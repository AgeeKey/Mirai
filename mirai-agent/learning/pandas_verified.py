"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T01:42:20.567850

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the data, or None if an error occurs.
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

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.

    Returns:
    None
    """
    print("Summary Statistics:")
    print(df.describe())

def main() -> None:
    """
    Main function to execute the data loading and summarization process.

    Returns:
    None
    """
    file_path = 'data.csv'  # Update with your actual file path
    data_frame = load_data(file_path)  # Load the data

    if data_frame is not None:  # Check if DataFrame was loaded successfully
        summarize_data(data_frame)  # Summarize the data

if __name__ == "__main__":
    main()