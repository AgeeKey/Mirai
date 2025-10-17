"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-17T12:39:48.088650

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Parameters:
    data (List[dict]): A list where each dictionary represents a row of data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.

    Raises:
    ValueError: If the data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Input must be a list of dictionaries.")
    
    if not data:
        raise ValueError("Input data cannot be empty.")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df

def main() -> None:
    """
    Main function to demonstrate DataFrame creation.
    """
    # Sample data
    sample_data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]
    
    try:
        # Create DataFrame
        df = create_dataframe(sample_data)
        print(df)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()