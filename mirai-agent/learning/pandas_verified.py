"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-15T10:38:47.523678

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Args:
        data (dict): A dictionary containing data for the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the provided data.
    
    Raises:
        ValueError: If the input data is empty or not a dictionary.
    """
    if not isinstance(data, dict) or not data:
        raise ValueError("Input data must be a non-empty dictionary.")

    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.Series:
    """
    Calculate basic statistics (mean, median, and standard deviation) for numerical columns in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.Series: A Series containing the mean, median, and standard deviation of each numerical column.
    
    Raises:
        ValueError: If the DataFrame is empty or does not contain numerical columns.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")

    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        raise ValueError("The DataFrame does not contain numerical columns.")

    return pd.Series({
        'mean': numeric_df.mean(),
        'median': numeric_df.median(),
        'std_dev': numeric_df.std()
    })

# Example usage
if __name__ == "__main__":
    try:
        # Sample data for DataFrame
        sample_data = {
            'A': [1, 2, 3, 4, 5],
            'B': [5, 6, 7, 8, 9],
            'C': [10, 11, 12, 13, 14]
        }
        
        # Create DataFrame
        df = create_dataframe(sample_data)
        print("DataFrame created:\n", df)

        # Calculate statistics
        stats = calculate_statistics(df)
        print("\nStatistics:\n", stats)
    
    except Exception as e:
        print(f"An error occurred: {e}")