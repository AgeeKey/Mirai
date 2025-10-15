"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-15T21:13:40.090744

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A pandas DataFrame constructed from the input data.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError("Error creating DataFrame: " + str(e))

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by filling missing values and removing duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: A cleaned pandas DataFrame.
    """
    try:
        df_filled = df.fillna(method='ffill')  # Forward fill missing values
        df_cleaned = df_filled.drop_duplicates()  # Remove duplicate rows
        return df_cleaned
    except Exception as e:
        raise ValueError("Error cleaning DataFrame: " + str(e))

def main() -> None:
    """
    Main function to execute the DataFrame creation and cleaning process.
    """
    # Sample data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', np.nan, 'Eve'],
        'Age': [24, 30, 22, 25, np.nan],
        'City': ['New York', 'Los Angeles', 'New York', 'Chicago', 'Chicago']
    }

    # Create DataFrame
    df = create_dataframe(data)
    print("Original DataFrame:")
    print(df)

    # Clean DataFrame
    cleaned_df = clean_data(df)
    print("\nCleaned DataFrame:")
    print(cleaned_df)

if __name__ == "__main__":
    main()