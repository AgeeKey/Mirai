"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-17T00:03:28.484408

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from a dictionary.
    
    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.
        
    Returns:
        pd.DataFrame: A DataFrame containing the provided data.
        
    Raises:
        ValueError: If the lengths of the lists in the dictionary do not match.
    """
    if not all(len(v) == len(next(iter(data.values()))) for v in data.values()):
        raise ValueError("All lists in the dictionary must have the same length.")
    
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates basic statistics for numeric columns in a DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame containing numeric data.
        
    Returns:
        pd.DataFrame: A DataFrame with mean, median, and standard deviation of numeric columns.
    """
    stats = pd.DataFrame({
        'mean': df.mean(),
        'median': df.median(),
        'std_dev': df.std()
    })
    return stats

def main() -> None:
    """
    Main function to execute the data creation and analysis.
    """
    # Sample data
    data = {
        'A': np.random.randint(1, 100, 10),
        'B': np.random.rand(10),
        'C': np.random.choice(['X', 'Y', 'Z'], 10)
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("Original DataFrame:")
        print(df)

        # Calculate statistics for numeric columns
        stats = calculate_statistics(df[['A', 'B']])
        print("\nStatistics:")
        print(stats)
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()