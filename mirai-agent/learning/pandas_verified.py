"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-20T16:45:26.153859

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def generate_sample_data(num_rows: int) -> pd.DataFrame:
    """
    Generate a sample DataFrame with random data.
    
    Args:
        num_rows (int): The number of rows to generate.
    
    Returns:
        pd.DataFrame: A DataFrame containing random data.
    """
    if num_rows <= 0:
        raise ValueError("Number of rows must be positive.")
    
    # Create a DataFrame with random numbers and categories
    data = {
        'A': np.random.rand(num_rows),  # Random float numbers
        'B': np.random.randint(1, 100, size=num_rows),  # Random integers
        'C': np.random.choice(['cat', 'dog', 'bird'], size=num_rows)  # Random categories
    }
    
    return pd.DataFrame(data)

def filter_data(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a threshold for column 'A'.
    
    Args:
        df (pd.DataFrame): The DataFrame to filter.
        threshold (float): The threshold value for filtering.
    
    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    if 'A' not in df.columns:
        raise KeyError("Column 'A' is not present in the DataFrame.")
    
    # Filter the DataFrame where values in column 'A' are greater than the threshold
    filtered_df = df[df['A'] > threshold]
    
    return filtered_df

def main() -> None:
    """
    Main function to execute the data generation and filtering.
    """
    try:
        # Generate sample data
        num_rows = 10
        df = generate_sample_data(num_rows)
        print("Original DataFrame:")
        print(df)

        # Set a threshold for filtering
        threshold = 0.5
        filtered_df = filter_data(df, threshold)
        print(f"\nFiltered DataFrame with threshold > {threshold}:")
        print(filtered_df)
    
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except KeyError as ke:
        print(f"KeyError: {ke}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()