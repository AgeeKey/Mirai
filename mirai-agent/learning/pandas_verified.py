"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-17T13:29:00.175580

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: DataFrame containing the loaded data.
    
    Raises:
    FileNotFoundError: If the specified file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data found in the file.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def analyze_data(df: pd.DataFrame, column: Optional[str] = None) -> None:
    """
    Analyze the DataFrame and print summary statistics for a specified column.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    column (Optional[str]): The column to summarize. If None, summarize all columns.

    Returns:
    None
    """
    if column and column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    # Display general information about the DataFrame
    print("DataFrame Info:")
    print(df.info())
    
    # Provide summary statistics
    print("\nSummary Statistics:")
    if column:
        print(df[column].describe())
    else:
        print(df.describe())

def main(file_path: str, column: Optional[str] = None) -> None:
    """
    Main function to load data and analyze it.

    Parameters:
    file_path (str): The path to the CSV file.
    column (Optional[str]): The column to summarize.
    
    Returns:
    None
    """
    df = load_data(file_path)
    analyze_data(df, column)

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your CSV file path
    column_name = 'Age'  # Replace with the column you want to analyze
    main(file_path, column_name)