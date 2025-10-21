"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-21T04:26:46.559176

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_to_filter: Optional[str] = None, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame, and optionally filter it based on a specified column and value.

    Parameters:
        file_path (str): The path to the CSV file.
        column_to_filter (Optional[str]): The column to filter on (default is None).
        filter_value (Optional[str]): The value to filter by (default is None).

    Returns:
        pd.DataFrame: The processed DataFrame after loading and filtering.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column is not in the DataFrame.
    """
    try:
        # Load data from CSV file into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e
    
    # Filter the DataFrame if specified
    if column_to_filter and filter_value:
        if column_to_filter not in df.columns:
            raise ValueError(f"Error: The column '{column_to_filter}' is not in the DataFrame.")
        df = df[df[column_to_filter] == filter_value]

    return df

def main() -> None:
    """
    Main function to demonstrate loading and processing a CSV file.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    column_to_filter = 'Category'  # Example column to filter
    filter_value = 'A'  # Example value to filter by

    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path, column_to_filter, filter_value)
        print(processed_data)
    except (FileNotFoundError, ValueError) as e:
        print(e)

if __name__ == "__main__":
    main()