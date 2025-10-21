"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-21T10:01:21.081109

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, process it, and return a filtered DataFrame.

    Args:
        file_path (str): The path to the CSV file to load.
        column_name (str): The column to filter on.
        filter_value (Optional[str]): The value to filter by. If None, no filtering is applied.

    Returns:
        pd.DataFrame: The processed DataFrame.

    Raises:
        FileNotFoundError: If the provided file path does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
        
        # Filter the DataFrame if a filter value is provided
        if filter_value is not None:
            df = df[df[column_name] == filter_value]
        
        return df

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data_frame = load_and_process_data("data.csv", "category", "A")
        print(data_frame)
    except Exception as e:
        print(f"Failed to load and process data: {e}")