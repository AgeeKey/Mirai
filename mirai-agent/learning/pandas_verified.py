"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-22T18:28:49.380075

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary of data.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.

    Raises:
    ValueError: If the lengths of the lists in the dictionary do not match.
    """
    # Check if all columns have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same number of rows.")

    # Create and return the DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Calculate basic statistics for each numeric column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.

    Returns:
    pd.Series: A Series containing the mean, median, and standard deviation for each numeric column.
    """
    # Check if the DataFrame is empty
    if df.empty:
        raise ValueError("The DataFrame is empty.")

    # Calculate statistics
    stats = pd.Series({
        'mean': df.mean(),
        'median': df.median(),
        'std_dev': df.std()
    })
    return stats

def main() -> None:
    """
    Main function to execute the data processing workflow.
    """
    # Sample data
    data = {
        'A': np.random.rand(10),
        'B': np.random.rand(10),
        'C': np.random.rand(10)
    }

    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame Created:\n", df)

        # Calculate statistics
        stats = calculate_statistics(df)
        print("Statistics:\n", stats)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()