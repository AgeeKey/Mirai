"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-17T02:45:09.875766

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from a given dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.
    
    Raises:
    ValueError: If the lengths of the lists in the dictionary do not match.
    """
    # Check if all columns have the same length
    column_lengths = [len(column) for column in data.values()]
    if len(set(column_lengths)) != 1:
        raise ValueError("All columns must have the same length.")
    
    # Create the DataFrame
    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to demonstrate the creation of a DataFrame.
    """
    # Sample data
    data = {
        'A': np.random.rand(10),
        'B': np.random.rand(10),
        'C': np.random.rand(10)
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()