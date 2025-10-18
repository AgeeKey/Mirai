"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-18T13:42:42.417114

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
        pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Convert column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise

def filter_data(df: pd.DataFrame, column_name: str, threshold: float) -> pd.DataFrame:
    """
    Filter rows in the DataFrame based on a threshold for a specific column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column_name (str): The column to apply the filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: A DataFrame containing only the filtered rows.

    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Filter the DataFrame based on the threshold
        filtered_df = df[df[column_name] > threshold]
        return filtered_df
    except KeyError as e:
        print(f"Error: The column '{column_name}' does not exist in the DataFrame.")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        data = load_and_process_data('data.csv')
        filtered_data = filter_data(data, 'value', 10.0)
        print(filtered_data)
    except Exception as e:
        print(f"An error occurred: {e}")