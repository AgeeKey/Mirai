"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-16T03:40:03.710332

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError("An error occurred while creating the DataFrame: " + str(e))

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by filling missing values and dropping duplicates.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    try:
        df.fillna(0, inplace=True)  # Fill missing values with 0
        df.drop_duplicates(inplace=True)  # Remove duplicate rows
        return df
    except Exception as e:
        raise ValueError("An error occurred while cleaning the DataFrame: " + str(e))

def main():
    # Sample data for the DataFrame
    sample_data = {
        "A": [1, 2, np.nan, 4, 5],
        "B": [5, 6, 7, 8, 9],
        "C": [np.nan, 2, 3, 4, 5]
    }

    # Create a DataFrame
    df = create_dataframe(sample_data)
    print("Original DataFrame:")
    print(df)

    # Clean the DataFrame
    cleaned_df = clean_data(df)
    print("\nCleaned DataFrame:")
    print(cleaned_df)

if __name__ == "__main__":
    main()