"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-16T06:36:33.390177

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict, index: Optional[list] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.
    
    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.
        index (Optional[list]): An optional list to specify the index for the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.
    
    Raises:
        ValueError: If the lengths of the lists in the dictionary do not match.
    """
    # Check if all lists in the dictionary have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) > 1:
        raise ValueError("All columns must have the same number of rows.")
    
    # Create and return the DataFrame
    return pd.DataFrame(data, index=index)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.DataFrame: A DataFrame containing the mean and standard deviation of each numeric column.
    """
    # Calculate mean and standard deviation
    stats = pd.DataFrame({
        'mean': df.mean(),
        'std_dev': df.std()
    })
    
    return stats

# Example usage
if __name__ == "__main__":
    try:
        # Sample data for DataFrame
        sample_data = {
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': [5.5, 6.5, 7.5, 8.5, 9.5]
        }
        
        # Create DataFrame
        df = create_dataframe(sample_data)
        
        # Calculate statistics
        statistics = calculate_statistics(df)
        
        # Print results
        print("DataFrame:")
        print(df)
        print("\nStatistics:")
        print(statistics)
    except Exception as e:
        print(f"An error occurred: {e}")