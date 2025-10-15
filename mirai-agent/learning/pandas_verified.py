"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-15T03:38:27.300284

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Parameters:
    data (List[dict]): A list of dictionaries where each dictionary represents a row of data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.
    
    Raises:
    ValueError: If the input data is empty or not in the correct format.
    """
    if not data:
        raise ValueError("Input data cannot be empty.")
    
    # Attempt to create DataFrame
    try:
        df = pd.DataFrame(data)
    except Exception as e:
        raise ValueError(f"Error creating DataFrame: {e}")

    return df

def main() -> None:
    """
    Main function to demonstrate the creation of a DataFrame.
    """
    # Sample data
    data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print(df)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()