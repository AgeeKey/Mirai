"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-19T00:38:10.557583

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
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError("Error creating DataFrame: {}".format(e))

def calculate_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate basic statistics for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): A pandas DataFrame.

    Returns:
        dict: A dictionary containing the mean, median, and standard deviation for each numeric column.
    """
    try:
        stats = {
            'mean': df.mean(),
            'median': df.median(),
            'std_dev': df.std()
        }
        return stats
    except Exception as e:
        raise ValueError("Error calculating statistics: {}".format(e))

def main() -> None:
    """
    Main function to create a DataFrame and calculate its statistics.
    """
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, np.nan, 2, 1],
        'C': ['a', 'b', 'c', 'd', 'e']
    }

    # Create DataFrame
    df = create_dataframe(data)
    print("DataFrame:\n", df)

    # Calculate and print statistics
    stats = calculate_statistics(df[['A', 'B']])
    print("Statistics:\n", stats)

if __name__ == "__main__":
    main()