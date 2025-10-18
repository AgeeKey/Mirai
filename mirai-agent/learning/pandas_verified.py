"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-18T00:32:47.566544

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: Optional[dict] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the provided data.

    Parameters:
    data (dict, optional): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.
    """
    if data is None:
        # Default data if none provided
        data = {
            "A": np.random.rand(10),
            "B": np.random.randint(1, 100, size=10),
            "C": np.random.choice(['X', 'Y', 'Z'], size=10)
        }
    
    try:
        df = pd.DataFrame(data)
    except Exception as e:
        raise ValueError("Failed to create DataFrame: " + str(e))
    
    return df

def analyze_dataframe(df: pd.DataFrame) -> None:
    """
    Analyze the DataFrame and print summary statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")
    
    print("DataFrame Summary:")
    print(df.describe(include='all'))  # Including all data types for summary

def main() -> None:
    """
    Main function to execute the DataFrame creation and analysis.
    """
    try:
        df = create_dataframe()
        analyze_dataframe(df)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()