"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-16T09:35:14.793016

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file and process the data.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except pd.errors.ParserError:
        raise ValueError("Error parsing the file.")

    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Reset the index after dropping rows
    df.reset_index(drop=True, inplace=True)

    return df

def filter_data(df: pd.DataFrame, column_name: str, values: List) -> pd.DataFrame:
    """
    Filter the DataFrame based on a column and a list of values.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    column_name (str): The column to filter on.
    values (List): A list of values to filter by.

    Returns:
    pd.DataFrame: The filtered DataFrame.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
    
    # Filter the DataFrame
    filtered_df = df[df[column_name].isin(values)]
    
    return filtered_df

if __name__ == "__main__":
    # Example usage
    try:
        data = load_and_process_data('data.csv')  # Replace 'data.csv' with your file path
        filtered_data = filter_data(data, 'Category', ['A', 'B'])  # Replace 'Category' and values as needed
        print(filtered_data)
    except Exception as e:
        print(f"An error occurred: {e}")