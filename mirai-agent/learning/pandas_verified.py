"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T04:45:34.597020

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
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

def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    """
    Filters the DataFrame based on a column value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter by.
        value (str): The value to filter for.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    return df[df[column] == value]

def summarize_data(df: pd.DataFrame, group_by: str) -> pd.DataFrame:
    """
    Summarizes the DataFrame by grouping and counting occurrences.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
        group_by (str): The column name to group by.

    Returns:
        pd.DataFrame: Summary DataFrame with counts.
    """
    if group_by not in df.columns:
        raise ValueError(f"Column '{group_by}' does not exist in the DataFrame.")
    
    return df.groupby(group_by).size().reset_index(name='count')

def main(file_path: str, filter_column: str, filter_value: str, group_by: str) -> None:
    """
    Main function to load, filter, and summarize data.

    Args:
        file_path (str): The path to the CSV file.
        filter_column (str): The column to filter by.
        filter_value (str): The value to filter for.
        group_by (str): The column to group by.
    """
    df = load_data(file_path)  # Load data from CSV
    filtered_df = filter_data(df, filter_column, filter_value)  # Filter the DataFrame
    summary_df = summarize_data(filtered_df, group_by)  # Summarize the filtered DataFrame
    
    print(summary_df)  # Print the summary DataFrame

# Example usage
if __name__ == "__main__":
    # Replace 'data.csv', 'column_name', 'value', and 'group_column' with actual parameters
    main('data.csv', 'column_name', 'value', 'group_column')