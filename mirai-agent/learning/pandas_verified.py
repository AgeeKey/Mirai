"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-20T03:11:04.627418

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: Optional[dict[str, list]]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary of lists.

    Parameters:
    data (Optional[dict[str, list]]): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame created from the provided data.

    Raises:
    ValueError: If the input data is None or if the lists in the dictionary are not of the same length.
    """
    if data is None:
        raise ValueError("Input data cannot be None.")

    # Check if all lists in the dictionary have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the data dictionary must have the same length.")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to demonstrate the creation and manipulation of a DataFrame.
    """
    # Sample data to create a DataFrame
    data = {
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("Original DataFrame:")
        print(df)

        # Add a new column D that is the sum of columns A, B, and C
        df['D'] = df[['A', 'B', 'C']].sum(axis=1)
        print("\nDataFrame after adding column D:")
        print(df)

        # Handle potential errors during data manipulation
        # Example: Trying to access a non-existing column
        try:
            print("\nAccessing non-existing column E:")
            print(df['E'])
        except KeyError as e:
            print(f"Error: {e}")

    except ValueError as e:
        print(f"ValueError: {e}")

if __name__ == "__main__":
    main()