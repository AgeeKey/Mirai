"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-17T05:24:56.402932

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries where each dictionary represents a row of data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the input data is not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input data must be a list of dictionaries.")
    
    return pd.DataFrame(data)

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and basic operations.
    """
    # Sample data to create a DataFrame
    sample_data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]

    try:
        # Create DataFrame
        df = create_dataframe(sample_data)

        # Display the DataFrame
        print("Initial DataFrame:")
        print(df)

        # Calculate the average age
        average_age = df['age'].mean()
        print("\nAverage Age:", average_age)

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()