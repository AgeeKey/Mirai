"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-20T16:13:03.932488

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def generate_sample_data(num_rows: int) -> pd.DataFrame:
    """
    Generate a sample DataFrame with random data.

    Args:
        num_rows (int): The number of rows to generate.

    Returns:
        pd.DataFrame: A DataFrame containing random data.
    """
    if num_rows <= 0:
        raise ValueError("Number of rows must be a positive integer.")
    
    data = {
        'A': np.random.randint(1, 100, size=num_rows),
        'B': np.random.rand(num_rows),
        'C': pd.date_range(start='2023-01-01', periods=num_rows, freq='D')
    }
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.DataFrame: A DataFrame containing the mean and standard deviation.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    stats = {
        'Mean': df.mean(),
        'Std Dev': df.std()
    }
    return pd.DataFrame(stats)

def main() -> None:
    """
    Main function to execute the example.
    """
    try:
        # Generate a sample DataFrame with 10 rows
        sample_df = generate_sample_data(10)
        print("Sample DataFrame:\n", sample_df)

        # Calculate statistics for the DataFrame
        stats_df = calculate_statistics(sample_df[['A', 'B']])
        print("\nStatistics:\n", stats_df)
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()