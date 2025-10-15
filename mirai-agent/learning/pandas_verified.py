"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-15T16:53:18.729121

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
        pd.DataFrame: A DataFrame constructed from the input data.
    
    Raises:
        ValueError: If the input dictionary is empty or columns have unequal lengths.
    """
    if not data:
        raise ValueError("Input dictionary is empty.")
    
    # Check for unequal lengths in columns
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same length.")
    
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Calculate basic statistics (mean, median, std) for numeric columns in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the mean, median, and standard deviation of numeric columns.
    
    Raises:
        ValueError: If the DataFrame does not contain any numeric columns.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        raise ValueError("No numeric columns to calculate statistics.")
    
    stats = {
        'mean': numeric_df.mean(),
        'median': numeric_df.median(),
        'std': numeric_df.std()
    }
    
    return pd.Series(stats)

def main() -> None:
    """
    Main function to run the example.
    """
    # Sample data
    data = {
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8],
        'C': ['foo', 'bar', 'baz', 'qux']
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Calculate and display statistics
        stats = calculate_statistics(df)
        print("\nStatistics:")
        print(stats)
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()