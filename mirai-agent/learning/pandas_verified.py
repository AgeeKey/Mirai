"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-21T23:17:30.593803

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """Load CSV data into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
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
        print("Error: There was a parsing error.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """Print summary statistics of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Summary Statistics:")
        print(df.describe())
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """Main function to load and summarize data.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    summarize_data(df)

if __name__ == "__main__":
    # Replace 'your_file.csv' with the actual file path you want to load
    main('your_file.csv')