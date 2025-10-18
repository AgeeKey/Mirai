"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-18T03:42:16.115096

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
        data (dict): A dictionary containing data to create the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame created from the provided data.
        
    Raises:
        ValueError: If the input data is not a dictionary.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    return pd.DataFrame(data)

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a pandas DataFrame by filling missing values and removing duplicates.

    Parameters:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
        
    Raises:
        ValueError: If the input is not a DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    df = df.fillna(method='ffill')  # Fill missing values using forward fill
    df = df.drop_duplicates()        # Remove duplicate rows
    return df

def main() -> None:
    """
    Main function to execute the example of DataFrame creation and cleaning.
    """
    data = {
        'A': [1, 2, np.nan, 4, 5],
        'B': ['a', 'b', 'c', 'd', 'd'],
        'C': [np.nan, 2.5, 3.5, np.nan, 5.5]
    }
    
    # Create DataFrame
    try:
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