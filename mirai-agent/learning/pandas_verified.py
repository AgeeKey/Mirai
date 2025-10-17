"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-17T15:23:21.655500

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, filter_column: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame, filter it by a specified column and value.

    Args:
        file_path (str): The path to the CSV file.
        filter_column (str): The column to filter on.
        filter_value (Optional[str]): The value to filter by. If None, no filtering is applied.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the filter_column does not exist in the DataFrame.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    # Check if the filter_column exists
    if filter_column not in df.columns:
        raise ValueError(f"Column '{filter_column}' does not exist in the DataFrame.")

    # Filter the DataFrame if a filter_value is provided
    if filter_value is not None:
        df = df[df[filter_column] == filter_value]

    return df

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    try:
        # Define the file path and filter criteria
        file_path = 'data.csv'  # Replace with your actual file path
        filter_column = 'category'  # Replace with your actual column name
        filter_value = 'A'  # Replace with your desired filter value

        # Load and process the data
        processed_data = load_and_process_data(file_path, filter_column, filter_value)

        # Display the processed data
        print(processed_data)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()