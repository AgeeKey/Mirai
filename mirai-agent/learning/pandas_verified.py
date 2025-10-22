"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 1/1
Learned: 2025-10-22T19:01:57.651408

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
        pd.DataFrame: A DataFrame containing the provided data.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def summarize_dataframe(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame including basic statistics.
    
    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    try:
        print("DataFrame Summary:")
        print(df.describe())
        print("\nDataFrame Info:")
        print(df.info())
    except Exception as e:
        print(f"Error summarizing DataFrame: {e}")

def main() -> None:
    """
    Main function to execute the DataFrame creation and summarization.
    """
    # Sample data for DataFrame creation
    data = {
        'A': np.random.rand(10),  # Column A with random floats
        'B': np.random.randint(1, 100, size=10),  # Column B with random integers
        'C': ['Category1', 'Category2'] * 5  # Column C with categorical data
    }
    
    # Create DataFrame
    df = create_dataframe(data)
    
    # Summarize DataFrame
    summarize_dataframe(df)

if __name__ == "__main__":
    main()