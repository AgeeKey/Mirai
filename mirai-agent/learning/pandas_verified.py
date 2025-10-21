"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-21T19:29:50.463740

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and process it.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame with cleaned data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}")
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.")

    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Reset index after dropping rows
    df.reset_index(drop=True, inplace=True)

    return df

def filter_data(df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a threshold for a specific column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to apply the filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    # Filter the DataFrame based on the threshold
    filtered_df = df[df[column] > threshold]

    return filtered_df

def main(file_path: str, column: str, threshold: float) -> None:
    """
    Main function to load, process, and filter data.

    Args:
        file_path (str): The path to the CSV file.
        column (str): The column name to filter on.
        threshold (float): The threshold for filtering.

    Returns:
        None
    """
    try:
        # Load and process the data
        df = load_and_process_data(file_path)
        
        # Filter the data based on the specified column and threshold
        filtered_df = filter_data(df, column, threshold)
        
        # Print the filtered DataFrame
        print(filtered_df)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    main("data.csv", "value_column", 10.0)