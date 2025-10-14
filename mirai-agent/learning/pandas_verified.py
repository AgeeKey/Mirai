"""
pandas - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-14T18:33:07.257236

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(rows: int, columns: int) -> pd.DataFrame:
    """
    Create a DataFrame with random numbers.

    Args:
        rows (int): Number of rows for the DataFrame.
        columns (int): Number of columns for the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame populated with random numbers.
    
    Raises:
        ValueError: If rows or columns are less than 1.
    """
    if rows < 1 or columns < 1:
        raise ValueError("Rows and columns must be greater than 0.")
    
    data = np.random.rand(rows, columns)  # Generate random numbers
    df = pd.DataFrame(data, columns=[f'Column_{i+1}' for i in range(columns)])  # Create DataFrame
    return df

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the mean and standard deviation for each column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the mean and std for each column.
    
    Raises:
        ValueError: If the input DataFrame is empty.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    stats = pd.DataFrame({
        'Mean': df.mean(),
        'Standard Deviation': df.std()
    })  # Calculate mean and std
    return stats

def main(rows: int, columns: int) -> None:
    """
    Main function to create a DataFrame and calculate its statistics.

    Args:
        rows (int): Number of rows for the DataFrame.
        columns (int): Number of columns for the DataFrame.
    """
    try:
        df = create_dataframe(rows, columns)  # Create DataFrame
        print("Generated DataFrame:")
        print(df)  # Print the DataFrame
        
        stats = calculate_statistics(df)  # Calculate statistics
        print("\nStatistics:")
        print(stats)  # Print statistics
    except ValueError as e:
        print(f"Error: {e}")  # Handle value errors

if __name__ == "__main__":
    main(5, 3)  # Example with 5 rows and 3 columns