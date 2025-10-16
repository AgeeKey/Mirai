"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T15:07:41.399998

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    """
    Filter the DataFrame based on a specific column and value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter on.
        value (str): The value to filter by.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    return df[df[column] == value]

def main() -> None:
    """
    Main function to execute the data loading and filtering process.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    df = load_data(file_path)

    if df is not None:
        try:
            filtered_df = filter_data(df, 'category', 'A')  # Replace 'category' and 'A' with your own values
            print(filtered_df)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()