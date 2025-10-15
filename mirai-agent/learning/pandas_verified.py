"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-15T17:42:07.487499

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(rows: int, columns: int) -> pd.DataFrame:
    """
    Create a DataFrame with random data.

    Parameters:
    rows (int): Number of rows in the DataFrame.
    columns (int): Number of columns in the DataFrame.

    Returns:
    pd.DataFrame: A DataFrame filled with random numbers.
    """
    if rows <= 0 or columns <= 0:
        raise ValueError("Number of rows and columns must be positive integers.")
    
    # Create a DataFrame with random numbers
    data = np.random.rand(rows, columns)
    df = pd.DataFrame(data, columns=[f'Col_{i+1}' for i in range(columns)])
    
    return df

def summarize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics for the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.

    Returns:
    pd.DataFrame: A DataFrame containing summary statistics.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    
    # Generate summary statistics
    summary = df.describe()
    
    return summary

def main() -> None:
    """
    Main function to execute the data manipulation example.
    """
    try:
        # Create a DataFrame with 5 rows and 3 columns
        df = create_dataframe(5, 3)
        print("Original DataFrame:")
        print(df)

        # Summarize the DataFrame
        summary = summarize_dataframe(df)
        print("\nSummary Statistics:")
        print(summary)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()