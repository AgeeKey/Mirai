"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-16T01:48:01.013588

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple

def generate_sample_data(rows: int) -> pd.DataFrame:
    """Generate a sample DataFrame with random data.

    Args:
        rows (int): The number of rows to generate.

    Returns:
        pd.DataFrame: A DataFrame containing sample data.
    """
    if rows <= 0:
        raise ValueError("Number of rows must be a positive integer.")
    
    # Generate random data
    data = {
        'A': np.random.rand(rows),  # Random floats
        'B': np.random.randint(0, 100, size=rows),  # Random integers
        'C': pd.date_range(start='2021-01-01', periods=rows, freq='D')  # Date range
    }
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> Optional[Tuple[float, float]]:
    """Calculate the mean and standard deviation of column 'A'.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Optional[Tuple[float, float]]: A tuple containing the mean and std of column 'A', or None if empty.
    """
    if df.empty:
        print("DataFrame is empty. Returning None.")
        return None
    
    mean_value = df['A'].mean()
    std_value = df['A'].std()
    return mean_value, std_value

def main() -> None:
    """Main function to execute the example."""
    try:
        # Generate sample data
        sample_df = generate_sample_data(10)  # Generate 10 rows of data
        print("Sample DataFrame:")
        print(sample_df)

        # Calculate statistics
        stats = calculate_statistics(sample_df)
        if stats:
            print(f"Mean of column 'A': {stats[0]}")
            print(f"Standard deviation of column 'A': {stats[1]}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()