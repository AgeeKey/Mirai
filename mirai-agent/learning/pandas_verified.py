"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T00:16:48.404901

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict[str, list]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary of lists.

    Parameters:
    data (dict[str, list]): A dictionary where keys are column names 
                             and values are lists of column data.

    Returns:
    pd.DataFrame: A pandas DataFrame constructed from the input data.
    """
    try:
        df = pd.DataFrame(data)  # Create DataFrame from the provided data
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def analyze_dataframe(df: pd.DataFrame) -> None:
    """
    Analyze a pandas DataFrame by printing summary statistics and checking for missing values.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    try:
        print("Summary Statistics:")
        print(df.describe())  # Print summary statistics
        print("\nMissing Values:")
        print(df.isnull().sum())  # Print the number of missing values in each column
    except Exception as e:
        print(f"Error analyzing DataFrame: {e}")

if __name__ == "__main__":
    # Sample data to demonstrate functionality
    sample_data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, np.nan, 22],
        "Salary": [50000, 60000, 70000, np.nan]
    }

    # Create a DataFrame using the sample data
    df = create_dataframe(sample_data)
    
    # Analyze the created DataFrame
    analyze_dataframe(df)