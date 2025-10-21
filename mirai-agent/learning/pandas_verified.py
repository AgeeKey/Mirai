"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-21T00:29:09.331844

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: list[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Args:
        data (list[dict]): A list of dictionaries containing data.

    Returns:
        pd.DataFrame: A DataFrame created from the input data.

    Raises:
        ValueError: If the input data is not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input must be a list of dictionaries.")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        None
    """
    # Display basic statistics of the DataFrame
    print("Basic Statistics:")
    print(df.describe())

    # Display null values in the DataFrame
    print("\nNull Values:")
    print(df.isnull().sum())

def main() -> None:
    """
    Main function to execute the DataFrame creation and analysis.

    Returns:
        None
    """
    # Sample data
    data = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 24, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": np.nan, "City": "Chicago"},
        {"Name": "David", "Age": 35, "City": "New York"}
    ]

    try:
        # Create DataFrame
        df = create_dataframe(data)
        
        # Analyze DataFrame
        analyze_data(df)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()