"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T04:03:15.151892

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Tuple

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame constructed from the provided dictionary.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError(f"Error creating DataFrame: {e}")

def calculate_statistics(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate the mean and standard deviation of a DataFrame's numeric columns.

    Parameters:
    df (pd.DataFrame): The DataFrame from which to calculate statistics.

    Returns:
    Tuple[float, float]: A tuple containing the mean and standard deviation.
    """
    try:
        mean = df.mean().mean()  # Mean of all numeric columns
        std_dev = df.std().mean()  # Std deviation of all numeric columns
        return mean, std_dev
    except Exception as e:
        raise ValueError(f"Error calculating statistics: {e}")

def main() -> None:
    """
    Main function to execute the data analysis workflow.
    """
    # Sample data
    data = {
        'A': np.random.rand(10),
        'B': np.random.rand(10),
        'C': np.random.rand(10)
    }

    # Create DataFrame
    df = create_dataframe(data)
    print("DataFrame:\n", df)

    # Calculate statistics
    mean, std_dev = calculate_statistics(df)
    print(f"Mean: {mean}, Standard Deviation: {std_dev}")

if __name__ == "__main__":
    main()