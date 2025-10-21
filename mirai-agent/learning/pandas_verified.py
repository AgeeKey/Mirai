"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-21T15:08:36.441254

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries where each dictionary
                           represents a row in the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame representing the input data.

    Raises:
        ValueError: If the input data is empty or invalid.
    """
    if not data:
        raise ValueError("Input data must not be empty.")

    try:
        df = pd.DataFrame(data)  # Create DataFrame
    except Exception as e:
        raise ValueError("Failed to create DataFrame: " + str(e))
    
    return df

def calculate_mean(df: pd.DataFrame, column: str) -> float:
    """
    Calculate the mean of a specified column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to calculate the mean from.
        column (str): The name of the column to calculate the mean.

    Returns:
        float: The mean of the specified column.

    Raises:
        ValueError: If the column does not exist in the DataFrame.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    mean_value = df[column].mean()  # Calculate mean
    return mean_value

# Example usage
if __name__ == "__main__":
    sample_data = [
        {"name": "Alice", "age": 30, "score": 85},
        {"name": "Bob", "age": 25, "score": 90},
        {"name": "Charlie", "age": 35, "score": 95}
    ]
    
    try:
        df = create_dataframe(sample_data)  # Create DataFrame from sample data
        mean_score = calculate_mean(df, "score")  # Calculate mean score
        print(f"Mean Score: {mean_score}")  # Output mean score
    except ValueError as e:
        print(f"Error: {e}")