"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-15T07:08:33.614935

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The loaded DataFrame.
    
    Raises:
    FileNotFoundError: If the file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: {e}")
        raise

def filter_data(df: pd.DataFrame, column_name: str, value: str) -> pd.DataFrame:
    """
    Filter the DataFrame based on a specific column and value.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    column_name (str): The column name to filter on.
    value (str): The value to filter by.

    Returns:
    pd.DataFrame: The filtered DataFrame.
    
    Raises:
    KeyError: If the column name does not exist in the DataFrame.
    """
    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' does not exist in the DataFrame.")
    return df[df[column_name] == value]

def main(file_path: str, column_name: str, value: str) -> None:
    """
    Main function to load, filter, and display data.

    Parameters:
    file_path (str): The path to the CSV file.
    column_name (str): The column name to filter on.
    value (str): The value to filter by.
    """
    # Load data from the CSV file
    df = load_data(file_path)
    
    # Filter the DataFrame
    filtered_df = filter_data(df, column_name, value)
    
    # Display the filtered DataFrame
    print(filtered_df)

if __name__ == "__main__":
    # Example usage
    main("data.csv", "category", "A")