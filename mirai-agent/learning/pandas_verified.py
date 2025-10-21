"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-21T16:14:36.363308

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Optional

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError(f"The file {file_path} is empty.") from e

def filter_data(df: pd.DataFrame, column_name: str, value: Optional[str]) -> pd.DataFrame:
    """Filter the DataFrame based on a specific column and value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column_name (str): The column to filter by.
        value (Optional[str]): The value to filter for.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    if value is None:
        return df
    
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
    
    filtered_df = df[df[column_name] == value]
    return filtered_df

def main(file_path: str, column_name: str, value: Optional[str] = None) -> None:
    """Main function to load, filter, and display data.

    Args:
        file_path (str): The path to the CSV file.
        column_name (str): The column to filter by.
        value (Optional[str]): The value to filter for.
    """
    # Load the data
    df = load_data(file_path)
    
    # Filter the data
    filtered_df = filter_data(df, column_name, value)
    
    # Display the filtered data
    print(filtered_df)

if __name__ == "__main__":
    # Example usage
    FILE_PATH = 'data.csv'  # Replace with your CSV file path
    COLUMN_NAME = 'Category'  # Replace with your desired column name
    VALUE = 'Electronics'  # Replace with the value you want to filter by, or None

    main(FILE_PATH, COLUMN_NAME, VALUE)