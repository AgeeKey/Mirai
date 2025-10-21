"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-21T08:25:22.990631

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, List

def create_dataframe(data: List[dict]) -> Optional[pd.DataFrame]:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Parameters:
        data (List[dict]): A list of dictionaries where the keys represent column names.

    Returns:
        Optional[pd.DataFrame]: A DataFrame constructed from the provided data, or None if data is empty.
    """
    if not data:
        print("Error: The input data list is empty.")
        return None
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return None

def main() -> None:
    """
    Main function to demonstrate DataFrame creation.
    """
    # Sample data to create DataFrame
    sample_data = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"},
    ]

    # Create the DataFrame
    df = create_dataframe(sample_data)

    if df is not None:
        print("DataFrame created successfully:")
        print(df)

if __name__ == "__main__":
    main()