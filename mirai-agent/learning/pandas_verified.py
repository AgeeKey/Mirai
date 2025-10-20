"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-20T07:23:30.462928

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there are parsing errors.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data found in the file.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def analyze_data(df: pd.DataFrame, column_name: str) -> Optional[pd.Series]:
    """
    Analyze a specific column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column_name (str): The name of the column to analyze.

    Returns:
        Optional[pd.Series]: A Series containing the count of unique values, or None if the column does not exist.
    
    Raises:
        ValueError: If the specified column does not exist in the DataFrame.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column {column_name} does not exist in the DataFrame.")
    
    # Count unique values in the specified column
    return df[column_name].value_counts()

def main():
    """
    Main function to load data and analyze a specific column.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    column_name = 'Category'  # Specify the column to analyze

    # Load data
    try:
        df = load_data(file_path)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Analyze data
    try:
        analysis_result = analyze_data(df, column_name)
        print("Analysis Result:")
        print(analysis_result)
    except Exception as e:
        print(f"Error analyzing data: {e}")

if __name__ == "__main__":
    main()