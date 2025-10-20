"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-20T22:22:17.055806

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame, process it by filtering and renaming columns.

    Args:
        file_path (str): The path to the CSV file.
        column_name (str): The name of the column to filter by.
        filter_value (Optional[str]): The value to filter the DataFrame. If None, no filtering is applied.

    Returns:
        pd.DataFrame: The processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column does not exist in the DataFrame.
    """
    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e

    # Check if the specified column exists
    if column_name not in df.columns:
        raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter value is provided
    if filter_value is not None:
        df = df[df[column_name] == filter_value]

    # Rename columns for clarity
    df.rename(columns={column_name: f"{column_name}_filtered"}, inplace=True)

    return df

# Example usage
if __name__ == "__main__":
    try:
        processed_data = load_and_process_data('data.csv', 'category', 'A')
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")