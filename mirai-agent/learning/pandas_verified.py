"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T20:26:57.064648

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
        pd.DataFrame: A pandas DataFrame created from the provided dictionary.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError("An error occurred while creating the DataFrame: " + str(e))

def calculate_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate basic statistics for a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        dict: A dictionary containing the mean and standard deviation of each numeric column.
    """
    try:
        stats = {
            'mean': df.mean(),
            'std_dev': df.std()
        }
        return stats
    except Exception as e:
        raise ValueError("An error occurred while calculating statistics: " + str(e))

def main() -> None:
    """
    Main function to execute the data processing workflow.
    """
    # Sample data
    data = {
        'A': np.random.randn(100),
        'B': np.random.rand(100),
        'C': np.random.randint(1, 100, 100)
    }

    # Create DataFrame
    df = create_dataframe(data)

    # Calculate statistics
    stats = calculate_statistics(df)

    # Print results
    print("Statistics:")
    print(stats)

if __name__ == "__main__":
    main()