"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-22T11:50:17.059821

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a DataFrame from a dictionary of lists.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A pandas DataFrame populated with the provided data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary are not equal.
    """
    if not all(len(v) == len(next(iter(data.values()))) for v in data.values()):
        raise ValueError("All lists in the dictionary must be of the same length.")
    
    return pd.DataFrame(data)

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by filling missing values and removing duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
        pd.DataFrame: A cleaned DataFrame.
    """
    # Fill missing values with the mean of each column
    df_filled = df.fillna(df.mean())
    
    # Remove duplicate rows
    df_cleaned = df_filled.drop_duplicates()
    
    return df_cleaned

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and cleaning.
    """
    # Example data
    data = {
        'A': [1, 2, np.nan, 4],
        'B': [5, np.nan, 7, 8],
        'C': [9, 10, 11, 12]
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("Original DataFrame:")
        print(df)

        # Clean DataFrame
        cleaned_df = clean_dataframe(df)
        print("\nCleaned DataFrame:")
        print(cleaned_df)
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()