"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-17T23:44:55.768595

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Optional

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Parameters:
    data (List[dict]): A list of dictionaries where each dictionary represents a row.

    Returns:
    pd.DataFrame: A pandas DataFrame constructed from the input data.
    
    Raises:
    ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Input must be a list of dictionaries.")
    
    if not data:
        raise ValueError("Input data cannot be empty.")
    
    return pd.DataFrame(data)

def filter_dataframe(df: pd.DataFrame, column: str, threshold: float) -> Optional[pd.DataFrame]:
    """
    Filter the DataFrame based on a threshold for a specific column.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    column (str): The column name to apply the filter on.
    threshold (float): The threshold value for filtering.

    Returns:
    Optional[pd.DataFrame]: A filtered DataFrame or None if the column does not exist.
    """
    if column not in df.columns:
        print(f"Column '{column}' does not exist in the DataFrame.")
        return None
    
    return df[df[column] > threshold]

# Example usage
if __name__ == "__main__":
    data = [
        {'name': 'Alice', 'age': 30, 'salary': 70000},
        {'name': 'Bob', 'age': 24, 'salary': 50000},
        {'name': 'Charlie', 'age': 35, 'salary': 80000}
    ]
    
    try:
        df = create_dataframe(data)
        print("Original DataFrame:")
        print(df)
        
        filtered_df = filter_dataframe(df, 'salary', 60000)
        if filtered_df is not None:
            print("\nFiltered DataFrame (salary > 60000):")
            print(filtered_df)
    except ValueError as e:
        print(f"Error: {e}")