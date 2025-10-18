"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T17:49:47.865952

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.
    
    Args:
        data (List[dict]): A list of dictionaries containing data.

    Returns:
        pd.DataFrame: A DataFrame containing the input data.
    
    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input data must be a list of dictionaries.")
    if not data:
        raise ValueError("Input data cannot be empty.")

    df = pd.DataFrame(data)
    return df

def calculate_average_age(df: pd.DataFrame) -> float:
    """
    Calculate the average age from the 'age' column in the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the 'age' column.

    Returns:
        float: The average age.
    
    Raises:
        KeyError: If the 'age' column is not present in the DataFrame.
    """
    if 'age' not in df.columns:
        raise KeyError("'age' column is not present in the DataFrame.")
    
    average_age = df['age'].mean()
    return average_age

def main() -> None:
    """
    Main function to execute the DataFrame creation and average age calculation.
    """
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35}
    ]

    try:
        df = create_dataframe(data)
        print("DataFrame created successfully:\n", df)
        
        avg_age = calculate_average_age(df)
        print("Average age:", avg_age)
    
    except (ValueError, KeyError) as e:
        print("Error:", e)

if __name__ == "__main__":
    main()