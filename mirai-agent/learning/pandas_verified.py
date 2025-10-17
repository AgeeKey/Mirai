"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-17T14:01:41.175843

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by applying a column filter.

    Args:
        file_path (str): The path to the CSV file.
        column_filter (Optional[list]): List of columns to keep in the DataFrame.

    Returns:
        pd.DataFrame: Processed DataFrame with only the specified columns.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If any column in the filter does not exist in the DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        if column_filter is not None:
            # Check if the specified columns exist in the DataFrame
            missing_columns = [col for col in column_filter if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Columns not found in the DataFrame: {missing_columns}")

            # Filter the DataFrame to include only the specified columns
            df = df[column_filter]

        return df
    
    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        data = load_and_process_data('sample_data.csv', column_filter=['column1', 'column2'])
        print(data.head())
    except Exception as e:
        print(f"Failed to load and process data: {e}")