"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-16T22:09:41.050718

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from pandas import DataFrame
from typing import List

def create_dataframe(data: List[dict]) -> DataFrame:
    """
    Create a Pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries where keys correspond to column names.

    Returns:
        DataFrame: A Pandas DataFrame created from the input data.

    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input must be a list of dictionaries.")
    if not data:
        raise ValueError("Input data cannot be empty.")

    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and manipulation.
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
        print("Initial DataFrame:")
        print(df)

        # Add a new column 'age_next_year'
        df['age_next_year'] = df['age'] + 1
        print("\nDataFrame after adding 'age_next_year':")
        print(df)

        # Filter DataFrame for ages greater than 30
        filtered_df = df[df['age'] > 30]
        print("\nFiltered DataFrame (age > 30):")
        print(filtered_df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()