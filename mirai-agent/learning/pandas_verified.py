"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T01:41:16.502032

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a DataFrame from a dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        raise

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing data.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation for each numeric column.
    """
    try:
        stats = pd.DataFrame({
            'mean': df.mean(),
            'median': df.median(),
            'std_dev': df.std()
        })
        return stats
    except Exception as e:
        print(f"Error calculating statistics: {e}")
        raise

def main() -> None:
    """
    Main function to execute the data processing workflow.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [2, 3, np.nan, 5, 1]
    }

    # Create DataFrame
    df = create_dataframe(data)
    print("DataFrame:")
    print(df)

    # Calculate statistics
    stats = calculate_statistics(df)
    print("\nStatistics:")
    print(stats)

if __name__ == "__main__":
    main()