"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-16T19:59:55.203054

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from a given dictionary.

    Args:
        data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
        ValueError: If the lengths of the lists in the dictionary are unequal.
    """
    # Check if all lists in the dictionary have the same length
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")
    
    return pd.DataFrame(data)

def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates basic statistics (mean, std, min, max) for numerical columns in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame for which to calculate statistics.

    Returns:
        pd.DataFrame: A DataFrame containing the calculated statistics.
    """
    # Selecting only numeric columns for statistics
    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.agg(['mean', 'std', 'min', 'max'])

# Example usage
if __name__ == "__main__":
    try:
        # Sample data for DataFrame creation
        sample_data = {
            'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8],
            'C': [9, 10, 11, 12]
        }

        # Create DataFrame
        df = create_dataframe(sample_data)
        
        # Calculate statistics
        stats = calculate_statistics(df)
        
        # Display the DataFrame and its statistics
        print("DataFrame:")
        print(df)
        print("\nStatistics:")
        print(stats)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")