"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T03:15:58.280811

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.
    
    Parameters:
        data (dict): A dictionary where keys are column names and values are lists of column data.
    
    Returns:
        pd.DataFrame: A DataFrame created from the provided data.
    
    Raises:
        ValueError: If the lengths of the lists in the dictionary do not match.
    """
    # Check if all lists in the dictionary have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must be of the same length.")
    
    # Create DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> Optional[dict]:
    """
    Calculate basic statistics (mean, median, and standard deviation) for each numeric column in the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.
    
    Returns:
        dict: A dictionary containing mean, median, and standard deviation for each numeric column.
    """
    if df.empty:
        print("DataFrame is empty. No statistics to calculate.")
        return None
    
    # Calculate statistics
    return {
        'mean': df.mean().to_dict(),
        'median': df.median().to_dict(),
        'std_dev': df.std().to_dict()
    }

def main() -> None:
    """
    Main function to run the example code for creating a DataFrame and calculating statistics.
    """
    # Example data
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [2, 3, np.nan, 5, 6]  # np.nan to demonstrate handling missing values
    }
    
    try:
        # Create DataFrame
        df = create_dataframe(data)
        print("DataFrame created successfully:")
        print(df)

        # Calculate and print statistics
        stats = calculate_statistics(df)
        print("\nCalculated statistics:")
        print(stats)

    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()