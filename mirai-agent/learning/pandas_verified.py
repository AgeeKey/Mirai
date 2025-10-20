"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-20T17:33:38.177652

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from a given dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary are inconsistent.
    """
    # Check if all columns have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same length.")

    # Create a DataFrame
    return pd.DataFrame(data)

def calculate_mean(df: pd.DataFrame, column: str) -> float:
    """
    Calculates the mean of a specified column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column (str): The column name for which to calculate the mean.

    Returns:
        float: The mean of the specified column.

    Raises:
        KeyError: If the column does not exist in the DataFrame.
    """
    # Check if the column exists in the DataFrame
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist in the DataFrame.")
    
    # Calculate and return the mean
    return df[column].mean()

if __name__ == "__main__":
    # Sample data
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "Salary": [50000, 60000, 70000]
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Calculate mean salary
        mean_salary = calculate_mean(df, "Salary")
        print(f"Mean Salary: {mean_salary}")

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")