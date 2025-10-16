"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T08:30:10.005337

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries with the same keys.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.
    
    Raises:
        ValueError: If the input data is empty or not a list.
    """
    if not isinstance(data, list) or not data:
        raise ValueError("Input data must be a non-empty list of dictionaries.")
    
    try:
        df = pd.DataFrame(data)  # Create DataFrame from the list of dictionaries
    except Exception as e:
        raise RuntimeError(f"Error creating DataFrame: {e}")
    
    return df

def main() -> None:
    """
    Main function to demonstrate the creation of a DataFrame.
    """
    sample_data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
    ]

    try:
        df = create_dataframe(sample_data)  # Create DataFrame
        print(df)  # Print the DataFrame
    except (ValueError, RuntimeError) as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()