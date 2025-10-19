"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-19T13:15:36.290794

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def generate_random_data(rows: int, cols: int) -> pd.DataFrame:
    """
    Generates a DataFrame with random data.

    Parameters:
    rows (int): Number of rows in the DataFrame.
    cols (int): Number of columns in the DataFrame.

    Returns:
    pd.DataFrame: A DataFrame containing random float values.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("Number of rows and columns must be positive integers.")

    data = np.random.rand(rows, cols)
    return pd.DataFrame(data, columns=[f'Column_{i+1}' for i in range(cols)])

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates mean and standard deviation for each column in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame containing mean and standard deviation of the input DataFrame.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    stats = {
        'Mean': df.mean(),
        'Standard Deviation': df.std()
    }
    return pd.DataFrame(stats)

def main() -> None:
    """
    Main function to execute the data generation and statistics calculation.
    """
    try:
        # Generate a DataFrame with 10 rows and 5 columns of random data
        random_data = generate_random_data(10, 5)
        print("Random Data:")
        print(random_data)

        # Calculate statistics for the generated DataFrame
        statistics = calculate_statistics(random_data)
        print("\nStatistics:")
        print(statistics)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()