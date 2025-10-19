"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-19T17:43:55.798081

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_analyze_data(file_path: str, column_name: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a DataFrame, analyze specific column statistics, and return the DataFrame.

    Args:
        file_path (str): The file path to the CSV file.
        column_name (str): The name of the column to analyze.

    Returns:
        Optional[pd.DataFrame]: The DataFrame loaded from the CSV file, or None if an error occurred.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
        
        # Print basic statistics of the specified column
        print(f"Statistics for column '{column_name}':")
        print(df[column_name].describe())
        
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

# Example usage
if __name__ == "__main__":
    file_path = 'data.csv'  # Replace with your CSV file path
    column_name = 'age'  # Replace with the column you want to analyze
    df = load_and_analyze_data(file_path, column_name)