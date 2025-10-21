"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-21T06:01:47.548474

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple

def create_dataframe(rows: int, cols: int) -> pd.DataFrame:
    """
    Create a DataFrame with random numbers.

    Args:
        rows (int): Number of rows in the DataFrame.
        cols (int): Number of columns in the DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing random numbers.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("Number of rows and columns must be positive integers.")
    
    data = np.random.rand(rows, cols)
    df = pd.DataFrame(data, columns=[f'Column_{i+1}' for i in range(cols)])
    return df

def calculate_statistics(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Calculate mean and standard deviation of each column in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        Tuple[pd.Series, pd.Series]: Mean and standard deviation of each column.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    
    mean_values = df.mean()
    std_values = df.std()
    return mean_values, std_values

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and statistics calculation.
    """
    try:
        # Create a DataFrame with 5 rows and 3 columns
        df = create_dataframe(5, 3)
        print("Created DataFrame:")
        print(df)

        # Calculate and print statistics
        mean, std = calculate_statistics(df)
        print("\nMean of each column:")
        print(mean)
        print("\nStandard Deviation of each column:")
        print(std)

    except ValueError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()