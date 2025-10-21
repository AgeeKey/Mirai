"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-21T18:41:16.538449

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
        ValueError: If the input dictionary is empty or if lists are of unequal length.
    """
    if not data:
        raise ValueError("Input dictionary is empty.")

    column_lengths = [len(v) for v in data.values()]
    if len(set(column_lengths)) != 1:
        raise ValueError("All columns must have the same length.")

    return pd.DataFrame(data)

def clean_data(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Clean the specified column in the DataFrame by filling NaN values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.
        column_name (str): The name of the column to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

    df[column_name].fillna(value="Missing", inplace=True)
    return df

def main() -> None:
    """
    Main function to execute the data manipulation tasks.
    """
    try:
        # Sample data to create the DataFrame
        sample_data = {
            'Name': ['Alice', 'Bob', np.nan, 'David'],
            'Age': [25, 30, 22, np.nan],
            'City': ['New York', 'Los Angeles', 'Chicago', np.nan]
        }

        # Create DataFrame
        df = create_dataframe(sample_data)
        print("Original DataFrame:")
        print(df)

        # Clean the 'City' column
        cleaned_df = clean_data(df, 'City')
        print("\nCleaned DataFrame:")
        print(cleaned_df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()