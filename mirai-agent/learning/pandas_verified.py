"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 1/1
Learned: 2025-10-22T18:12:09.779308

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def create_dataframe(data: List[Dict[str, any]]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (List[Dict[str, any]]): A list of dictionaries where each dictionary represents a row of data.

    Returns:
        pd.DataFrame: A DataFrame containing the data.
    
    Raises:
        ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Input must be a list of dictionaries.")
    if not data:
        raise ValueError("Input data cannot be empty.")
    
    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and manipulation.
    """
    # Sample data
    data = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("Initial DataFrame:")
        print(df)

        # Add a new column
        df['Salary'] = [70000, 80000, 90000]
        print("\nDataFrame after adding Salary column:")
        print(df)

        # Filter DataFrame for Age > 30
        filtered_df = df[df['Age'] > 30]
        print("\nFiltered DataFrame (Age > 30):")
        print(filtered_df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()