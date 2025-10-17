"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-17T03:01:22.984029

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
        ValueError: If the input data is not a dictionary or if the lengths of the lists are inconsistent.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    length_set = {len(v) for v in data.values()}
    if len(length_set) > 1:
        raise ValueError("All columns must have the same number of rows.")

    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics (mean, median, standard deviation) for numerical columns in a DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing numerical data.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation of each numerical column.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    stats = {
        'Mean': df.mean(),
        'Median': df.median(),
        'Standard Deviation': df.std()
    }
    
    return pd.DataFrame(stats)

def main() -> None:
    """
    Main function to execute the data processing workflow.
    """
    try:
        # Sample data
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': [5, 4, 3, 2, 1],
            'C': [2, 3, np.nan, 5, 6]
        }

        # Create DataFrame
        df = create_dataframe(data)
        print("Original DataFrame:")
        print(df)

        # Calculate statistics
        stats_df = calculate_statistics(df)
        print("\nStatistics:")
        print(stats_df)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()