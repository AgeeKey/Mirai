"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T06:56:48.796438

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("Error: The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error: There was a parsing error.") from e

def filter_data(df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a threshold for a specified column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to apply the filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: The filtered DataFrame.

    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    if column not in df.columns:
        raise KeyError(f"Error: The column '{column}' does not exist in the DataFrame.")
    
    filtered_df = df[df[column] > threshold]
    return filtered_df

def main(file_path: str, column: str, threshold: float) -> None:
    """
    Main function to load data, filter it, and display the result.

    Args:
        file_path (str): The path to the CSV file.
        column (str): The column name to filter on.
        threshold (float): The threshold value for filtering.
    """
    try:
        df = load_data(file_path)  # Load the data
        filtered_df = filter_data(df, column, threshold)  # Filter the DataFrame
        print(filtered_df)  # Display the filtered DataFrame
    except Exception as e:
        print(e)  # Print any errors that occur

if __name__ == "__main__":
    # Example usage
    main("data.csv", "age", 30.0)  # Modify the file path and parameters as needed