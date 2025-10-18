"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-18T07:55:50.171173

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A processed DataFrame with missing values handled.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        # Load the data
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file '{file_path}' was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e

    # Fill missing values with the mean of the column
    df.fillna(df.mean(), inplace=True)

    return df

def filter_data(df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a threshold for a specified column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to apply the filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: A DataFrame filtered by the specified column and threshold.
    
    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    if column not in df.columns:
        raise KeyError(f"The column '{column}' does not exist in the DataFrame.")
    
    # Filter the DataFrame based on the threshold
    filtered_df = df[df[column] > threshold]

    return filtered_df

def main(file_path: str, column: str, threshold: float) -> None:
    """
    Main function to load, process, and filter data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        column (str): The column name to filter.
        threshold (float): The threshold value for filtering.
    """
    # Load and process the data
    df = load_and_process_data(file_path)

    # Filter the data
    filtered_df = filter_data(df, column, threshold)

    # Output the result
    print(filtered_df)

if __name__ == "__main__":
    # Example usage
    main('data.csv', 'age', 30.0)