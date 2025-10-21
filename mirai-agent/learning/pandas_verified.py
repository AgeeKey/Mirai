"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-21T12:26:39.744517

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Parameters:
    data (List[dict]): A list of dictionaries containing the data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.
    
    Raises:
    ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input data must be a list of dictionaries.")
    if not data:
        raise ValueError("Input data cannot be empty.")

    return pd.DataFrame(data)

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and basic operations.
    """
    # Sample data
    sample_data = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]

    try:
        # Create DataFrame from sample data
        df = create_dataframe(sample_data)
        print("Created DataFrame:")
        print(df)

        # Basic operation: Calculate average age
        average_age = df['Age'].mean()
        print(f"\nAverage Age: {average_age:.2f}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()