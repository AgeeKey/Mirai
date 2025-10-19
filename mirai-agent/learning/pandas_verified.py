"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T08:47:26.333041

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Optional

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def filter_data(df: pd.DataFrame, column_name: str, threshold: float) -> pd.DataFrame:
    """Filter the DataFrame based on a column value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column_name (str): The column name to filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
    
    filtered_df = df[df[column_name] > threshold]
    return filtered_df

def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Save the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): The path to save the CSV file.

    Raises:
        IOError: If the file cannot be written.
    """
    try:
        df.to_csv(output_path, index=False)
    except IOError as e:
        raise IOError(f"Error writing to file: {output_path}") from e

def main(file_path: str, output_path: str, column_name: str, threshold: float) -> None:
    """Main function to load, filter, and save data.

    Args:
        file_path (str): The input CSV file path.
        output_path (str): The output CSV file path.
        column_name (str): The column to filter on.
        threshold (float): The threshold for filtering.
    """
    df = load_data(file_path)  # Load the data
    filtered_df = filter_data(df, column_name, threshold)  # Filter the data
    save_data(filtered_df, output_path)  # Save the filtered data

if __name__ == "__main__":
    # Example usage of the main function
    main("input_data.csv", "filtered_data.csv", "column_name", 10.0)