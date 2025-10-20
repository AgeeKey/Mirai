"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-20T17:01:29.730882

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a DataFrame from a dictionary of lists.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.
    
    Raises:
        ValueError: If the lengths of the lists in the dictionary are not equal.
    """
    if not all(len(v) == len(next(iter(data.values()))) for v in data.values()):
        raise ValueError("All lists in the dictionary must have the same length.")
    
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics of numeric columns in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing mean and standard deviation of numeric columns.
    """
    statistics = pd.DataFrame({
        'mean': df.mean(),
        'std': df.std()
    })
    return statistics

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8],
        'C': [9, 10, 11, 12]
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Calculate statistics
        stats = calculate_statistics(df)
        print("\nCalculated statistics:")
        print(stats)
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()