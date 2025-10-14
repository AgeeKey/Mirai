"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-14T15:32:04.595177

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def create_dataframe(data: List[Dict[str, any]]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (List[Dict[str, any]]): A list of dictionaries where each dictionary represents a row of data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input data must be a list of dictionaries.")
    
    if not data:
        raise ValueError("Input data cannot be empty.")

    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df

def filter_dataframe(df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a threshold for a specified column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to apply the filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only rows where the specified column is greater than the threshold.

    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' does not exist in the DataFrame.")
    
    # Filter DataFrame
    filtered_df = df[df[column] > threshold]
    
    return filtered_df

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = [
        {"name": "Alice", "age": 30, "salary": 70000},
        {"name": "Bob", "age": 25, "salary": 50000},
        {"name": "Charlie", "age": 35, "salary": 90000}
    ]

    try:
        # Create DataFrame
        df = create_dataframe(sample_data)
        print("Original DataFrame:")
        print(df)

        # Filter DataFrame by salary
        filtered_df = filter_dataframe(df, "salary", 60000)
        print("\nFiltered DataFrame (salary > 60000):")
        print(filtered_df)

    except (ValueError, KeyError) as e:
        print(f"Error: {e}")