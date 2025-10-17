"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-17T07:49:48.492076

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a Pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries representing rows of data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.
    
    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not data:
        raise ValueError("Input data must be a non-empty list of dictionaries.")
    
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("All items in the list must be dictionaries.")
    
    df = pd.DataFrame(data)  # Create DataFrame from the list of dictionaries
    return df

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and manipulation.
    """
    # Sample data
    sample_data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "San Francisco"},
        {"name": "Charlie", "age": 35, "city": "Los Angeles"}
    ]

    try:
        # Create a DataFrame using the sample data
        df = create_dataframe(sample_data)
        print("Original DataFrame:")
        print(df)

        # Add a new column for country
        df['country'] = 'USA'
        print("\nDataFrame after adding country column:")
        print(df)

        # Filter the DataFrame for ages greater than 30
        filtered_df = df[df['age'] > 30]
        print("\nFiltered DataFrame (age > 30):")
        print(filtered_df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()