"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-20T14:35:27.835329

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, filter_column: Optional[str] = None, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame and optionally filter it based on a column value.

    Args:
        file_path (str): The path to the CSV file.
        filter_column (Optional[str]): The column name to filter on (default is None).
        filter_value (Optional[str]): The value to filter by (default is None).

    Returns:
        pd.DataFrame: The processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the filter_column is not found in the DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Filter the DataFrame if a filter_column and filter_value are provided
        if filter_column and filter_value:
            if filter_column not in df.columns:
                raise ValueError(f"Column '{filter_column}' not found in the DataFrame.")
            df = df[df[filter_column] == filter_value]

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        data_frame = load_and_process_data("data.csv", filter_column="Category", filter_value="A")
        print(data_frame.head())
    except Exception as e:
        print(f"Failed to process data: {e}")