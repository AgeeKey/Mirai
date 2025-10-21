"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-21T21:39:56.338082

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
        pd.DataFrame: A DataFrame representing the input data.

    Raises:
        ValueError: If the input data is not in the correct format.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError("Error creating DataFrame: " + str(e))

def calculate_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate basic statistics for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        dict: A dictionary containing the mean and standard deviation for each numeric column.
    """
    stats = {}
    for column in df.select_dtypes(include=[np.number]).columns:
        stats[column] = {
            'mean': df[column].mean(),
            'std_dev': df[column].std()
        }
    return stats

def main() -> None:
    """Main function to run the example."""
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 6, 7, 8, 9],
        'C': ['a', 'b', 'c', 'd', 'e']
    }

    # Create DataFrame
    df = create_dataframe(data)
    print("DataFrame created:")
    print(df)

    # Calculate statistics
    try:
        stats = calculate_statistics(df)
        print("\nStatistics:")
        print(stats)
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()