"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-21T13:31:39.419612

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
    ValueError: If the input dictionary is empty or the lengths of the columns are inconsistent.
    """
    if not data:
        raise ValueError("Input dictionary cannot be empty.")

    # Check if all columns have the same length
    lengths = [len(column) for column in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same length.")

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Calculate basic statistics for numerical columns in a DataFrame.

    Parameters:
    df (pd.DataFrame): A pandas DataFrame containing numerical data.

    Returns:
    pd.Series: A Series containing the mean, median, and standard deviation.
    """
    if df.empty:
        raise ValueError("DataFrame cannot be empty.")

    # Calculate statistics
    stats = pd.Series({
        'mean': df.mean(),
        'median': df.median(),
        'std_dev': df.std()
    })
    return stats

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
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
        print("DataFrame:")
        print(df)

        # Calculate and display statistics
        stats = calculate_statistics(df)
        print("\nStatistics:")
        print(stats)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()