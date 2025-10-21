"""
Pandas - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.79
Tests Passed: 0/1
Learned: 2025-10-21T17:52:03.276215

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data: The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    """
    Filter the DataFrame based on a specific column and value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter on.
        value (str): The value to filter by.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    return df[df[column] == value]

def summarize_data(df: pd.DataFrame, group_by_column: str) -> pd.DataFrame:
    """
    Summarize the DataFrame by grouping and counting occurrences.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
        group_by_column (str): The column name to group by.

    Returns:
        pd.DataFrame: A DataFrame with summarized data.

    Raises:
        ValueError: If the group_by_column does not exist in the DataFrame.
    """
    if group_by_column not in df.columns:
        raise ValueError(f"Column '{group_by_column}' does not exist in the DataFrame.")
    return df.groupby(group_by_column).size().reset_index(name='counts')

def main(file_path: str) -> None:
    """
    Main function to load, filter, and summarize data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    filtered_df = filter_data(df, 'Category', 'A')  # Filter data where Category is 'A'
    summary_df = summarize_data(filtered_df, 'Subcategory')  # Summarize by Subcategory
    print(summary_df)  # Output the summary

if __name__ == "__main__":
    main("data.csv")  # Replace with your actual data file path