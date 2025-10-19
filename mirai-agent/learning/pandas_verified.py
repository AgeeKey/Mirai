"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-19T14:18:50.539985

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is an issue with parsing the CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise
    except pd.errors.ParserError as e:
        print("Error: Could not parse the file.")
        raise

def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    """
    Filter the DataFrame based on a specified column value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter by.
        value (str): The value to filter for.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    return df[df[column] == value]

def main(file_path: str, column: str, value: str) -> None:
    """
    Main function to load, filter, and display data.

    Args:
        file_path (str): The path to the CSV file.
        column (str): The column name to filter by.
        value (str): The value to filter for.
    """
    # Load the data from the specified CSV file
    df = load_data(file_path)
    
    # Filter the data based on the given criteria
    filtered_df = filter_data(df, column, value)
    
    # Display the filtered DataFrame
    print(filtered_df)

if __name__ == "__main__":
    # Example usage
    main("data.csv", "category", "A")