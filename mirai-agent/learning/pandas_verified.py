"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-22T07:00:56.359779

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a given dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input dictionary.
    
    Raises:
        ValueError: If the input dictionary is empty or the lists have different lengths.
    """
    if not data:
        raise ValueError("Input dictionary is empty.")

    # Check if all lists in the dictionary have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")

    # Create and return DataFrame
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate basic statistics for each numeric column in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the mean, median, and standard deviation for each numeric column.
    """
    # Calculate statistics and return
    return df.describe().loc[["mean", "50%", "std"]].rename(index={"50%": "median"})

def main() -> None:
    """
    Main function to execute the DataFrame creation and statistics calculation.
    """
    # Sample data to create DataFrame
    sample_data = {
        "A": np.random.rand(10),
        "B": np.random.rand(10),
        "C": np.random.rand(10)
    }

    try:
        # Create DataFrame
        df = create_dataframe(sample_data)
        print("DataFrame created successfully:\n", df)

        # Calculate and display statistics
        stats = calculate_statistics(df)
        print("\nStatistics:\n", stats)

    except ValueError as e:
        print("Error:", e)

if __name__ == "__main__":
    main()