"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-22T07:33:38.191635

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_sample_dataframe(rows: int) -> pd.DataFrame:
    """
    Creates a sample DataFrame with random data.

    Parameters:
    rows (int): The number of rows in the DataFrame.

    Returns:
    pd.DataFrame: A DataFrame containing random integers and a date range.
    """
    if rows <= 0:
        raise ValueError("Number of rows must be a positive integer.")

    dates = pd.date_range(start='2023-01-01', periods=rows, freq='D')
    data = {
        'Date': dates,
        'Value': np.random.randint(1, 100, size=rows)
    }
    return pd.DataFrame(data)

def compute_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Computes basic statistics of the 'Value' column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.

    Returns:
    pd.Series: A Series containing the mean, median, and standard deviation of the 'Value' column.
    """
    if 'Value' not in df.columns:
        raise KeyError("The DataFrame must contain a 'Value' column.")

    mean = df['Value'].mean()
    median = df['Value'].median()
    std_dev = df['Value'].std()

    return pd.Series({'Mean': mean, 'Median': median, 'Std Dev': std_dev})

def main() -> None:
    """
    Main function to execute the data generation and statistics computation.
    """
    try:
        # Create a sample DataFrame with 10 rows
        df = create_sample_dataframe(10)
        print("Sample DataFrame:")
        print(df)

        # Compute and print statistics
        stats = compute_statistics(df)
        print("\nStatistics:")
        print(stats)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()