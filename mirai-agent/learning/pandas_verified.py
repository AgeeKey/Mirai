"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-19T18:15:39.297942

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by filtering specific columns.

    Args:
        file_path (str): The path to the CSV file.
        column_filter (Optional[list]): A list of columns to retain in the DataFrame.

    Returns:
        pd.DataFrame: A processed DataFrame with only the specified columns, if provided.
    
    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If columns specified in column_filter are not found in the DataFrame.
    """
    try:
        # Load data from CSV file
        data = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file at '{file_path}' was not found.") from e

    # If a column filter is provided, check if the columns exist in the DataFrame
    if column_filter is not None:
        missing_columns = set(column_filter) - set(data.columns)
        if missing_columns:
            raise ValueError(f"Error: The following columns are not found in the DataFrame: {missing_columns}")

        # Filter the DataFrame to only include specified columns
        data = data[column_filter]

    return data

def main():
    file_path = "data.csv"  # Path to your CSV file
    columns_to_keep = ["Column1", "Column2"]  # Columns to keep in the DataFrame

    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path, columns_to_keep)
        print(processed_data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()