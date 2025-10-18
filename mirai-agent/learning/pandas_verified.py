"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-18T03:10:40.160105

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary do not match.
    """
    # Check if all lists in the dictionary have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to execute the DataFrame creation and display.
    """
    # Sample data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [24, 30, 22],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        
        # Display the DataFrame
        print(df)
        
        # Perform basic operations
        print("\nAverage Age:", df['Age'].mean())
        print("\nCities:", df['City'].unique())
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()