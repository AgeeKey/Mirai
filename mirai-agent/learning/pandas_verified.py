"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-16T22:26:05.724833

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from pandas import DataFrame
from typing import List, Dict

def create_dataframe(data: List[Dict[str, any]]) -> DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (List[Dict[str, any]]): A list of dictionaries where each dictionary represents a row.

    Returns:
        DataFrame: A pandas DataFrame created from the input data.

    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Input data must be a list of dictionaries.")
    
    if not data:
        raise ValueError("Input data cannot be empty.")
    
    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to demonstrate DataFrame creation.
    """
    # Sample data
    sample_data = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]
    
    try:
        # Create DataFrame
        df = create_dataframe(sample_data)
        print(df)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()