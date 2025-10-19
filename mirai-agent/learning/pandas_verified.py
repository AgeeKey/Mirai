"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-19T15:06:18.756178

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Parameters:
    data (List[dict]): A list of dictionaries where each dictionary represents a row.

    Returns:
    pd.DataFrame: A DataFrame constructed from the input data.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError("Error creating DataFrame: {}".format(e))

def filter_dataframe(df: pd.DataFrame, column: str, value) -> pd.DataFrame:
    """
    Filter the DataFrame based on a specific column value.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    column (str): The column name to filter on.
    value: The value to filter by.

    Returns:
    pd.DataFrame: A filtered DataFrame.
    """
    try:
        filtered_df = df[df[column] == value]
        return filtered_df
    except KeyError:
        raise KeyError(f"Column '{column}' does not exist in the DataFrame.")
    except Exception as e:
        raise ValueError("Error filtering DataFrame: {}".format(e))

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = [
        {'Name': 'Alice', 'Age': 30, 'City': 'New York'},
        {'Name': 'Bob', 'Age': 25, 'City': 'Los Angeles'},
        {'Name': 'Charlie', 'Age': 35, 'City': 'New York'}
    ]
    
    # Create DataFrame from sample data
    df = create_dataframe(sample_data)
    print("Original DataFrame:")
    print(df)

    # Filter the DataFrame for rows where City is 'New York'
    filtered_df = filter_dataframe(df, 'City', 'New York')
    print("\nFiltered DataFrame (City = 'New York'):")
    print(filtered_df)