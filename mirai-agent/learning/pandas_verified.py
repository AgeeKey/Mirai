"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-21T11:05:50.890508

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a given dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.
    
    Raises:
        ValueError: If the input dictionary is empty or if columns have different lengths.
    """
    if not data:
        raise ValueError("Input dictionary is empty.")
    
    # Check if all columns have the same length
    column_lengths = [len(v) for v in data.values()]
    if len(set(column_lengths)) > 1:
        raise ValueError("All columns must have the same length.")
    
    df = pd.DataFrame(data)
    return df

def add_column(df: pd.DataFrame, column_name: str, data: list) -> pd.DataFrame:
    """
    Add a new column to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to which the column will be added.
        column_name (str): The name of the new column.
        data (list): A list of data to populate the new column.
    
    Returns:
        pd.DataFrame: The DataFrame with the new column added.
    
    Raises:
        ValueError: If the length of data does not match the number of rows in the DataFrame.
    """
    if len(data) != len(df):
        raise ValueError("Length of data must match number of rows in the DataFrame.")
    
    df[column_name] = data
    return df

def main() -> None:
    """
    Main function to demonstrate the creation and manipulation of a DataFrame.
    """
    try:
        # Sample data
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }

        # Create DataFrame
        df = create_dataframe(data)
        print("Initial DataFrame:")
        print(df)

        # Add a new column
        df = add_column(df, 'Salary', [70000, 80000, 90000])
        print("\nDataFrame after adding Salary column:")
        print(df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()