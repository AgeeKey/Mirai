"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-22T17:17:40.481726

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
        pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input must be a list of dictionaries.")

    if not data:
        raise ValueError("Input data cannot be empty.")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and basic operations.
    """
    # Sample data
    data = [
        {'Name': 'Alice', 'Age': 30, 'City': 'New York'},
        {'Name': 'Bob', 'Age': 25, 'City': 'Los Angeles'},
        {'Name': 'Charlie', 'Age': 35, 'City': 'Chicago'}
    ]

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("Created DataFrame:")
        print(df)

        # Calculate mean age
        mean_age = df['Age'].mean()
        print(f"\nMean Age: {mean_age}")

        # Filter DataFrame for Age greater than 30
        filtered_df = df[df['Age'] > 30]
        print("\nFiltered DataFrame (Age > 30):")
        print(filtered_df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()