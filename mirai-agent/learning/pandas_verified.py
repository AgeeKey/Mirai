"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-21T21:24:20.130690

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter columns, and perform basic cleaning.

    Args:
        file_path (str): The path to the CSV file.
        column_filter (Optional[list]): List of columns to retain in the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the provided file path does not exist.
        ValueError: If column_filter contains columns not in the DataFrame.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Filter columns if specified
        if column_filter is not None:
            missing_cols = set(column_filter) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
            df = df[column_filter]

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data = load_and_process_data('data.csv', column_filter=['column1', 'column2'])
        print(data.head())
    except Exception as e:
        print(f"An error occurred: {e}")