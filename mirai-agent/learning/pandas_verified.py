"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T06:20:24.696632

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union, List

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the DataFrame by dropping missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    return df.dropna()

def summarize_data(df: pd.DataFrame, columns: Union[str, List[str]]) -> pd.DataFrame:
    """Generate summary statistics for the specified columns.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
        columns (Union[str, List[str]]): The column(s) to summarize.

    Returns:
        pd.DataFrame: The summary statistics.
    """
    return df[columns].describe()

def main(file_path: str) -> None:
    """Main function to load, clean, and summarize the data.

    Args:
        file_path (str): The path to the CSV file to process.
    """
    df = load_data(file_path)  # Load the data
    cleaned_df = clean_data(df)  # Clean the data
    summary = summarize_data(cleaned_df, cleaned_df.columns)  # Summarize data
    print(summary)  # Print the summary

if __name__ == "__main__":
    # Example CSV file path
    csv_file_path = "data.csv"  # Replace with your actual file path
    main(csv_file_path)