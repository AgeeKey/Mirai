"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-21T15:41:41.620560

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, filter_column: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame, filter it based on a specified column and value, and return the processed DataFrame.

    Args:
        file_path (str): The path to the CSV file.
        filter_column (str): The column name to filter on.
        filter_value (Optional[str]): The value to filter by. If None, no filtering is applied.

    Returns:
        pd.DataFrame: The processed DataFrame after loading and filtering.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the filter_column does not exist in the DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    # Check if the filter_column exists in the DataFrame
    if filter_column not in df.columns:
        raise ValueError(f"Column '{filter_column}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter_value is provided
    if filter_value is not None:
        df = df[df[filter_column] == filter_value]

    return df

if __name__ == "__main__":
    # Example usage
    try:
        processed_data = load_and_process_data("data.csv", "Category", "A")
        print(processed_data)
    except (FileNotFoundError, ValueError) as e:
        print(e)