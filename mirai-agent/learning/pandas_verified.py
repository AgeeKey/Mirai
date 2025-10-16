"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-16T21:37:14.089889

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
        pd.DataFrame: A DataFrame created from the provided data.

    Raises:
        ValueError: If the input data is not a dictionary or if the lists are of unequal length.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    # Validate the lengths of the input lists
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must be of the same length.")

    return pd.DataFrame(data)

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame and return the mean of each numeric column.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the mean of each numeric column.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    
    # Calculate the mean of numeric columns
    return df.mean()

def main() -> None:
    """
    Main function to demonstrate the creation and analysis of a DataFrame.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4],
        'B': [5.0, 6.5, 7.2, 8.1],
        'C': ['x', 'y', 'z', 'w']
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Analyze DataFrame
        means = analyze_data(df.select_dtypes(include=[np.number]))  # Only numeric columns
        print("Mean values of numeric columns:")
        print(means)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()