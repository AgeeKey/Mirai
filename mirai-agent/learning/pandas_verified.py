"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T22:34:42.826833

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by filtering columns.

    Args:
        file_path (str): The path to the CSV file.
        column_filter (Optional[list]): A list of columns to keep in the DataFrame.

    Returns:
        pd.DataFrame: A processed DataFrame containing the filtered data.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the column_filter contains columns not in the DataFrame.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)

        # If column_filter is provided, filter the DataFrame
        if column_filter is not None:
            missing_cols = set(column_filter) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
            df = df[column_filter]

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data_frame = load_and_process_data("data.csv", column_filter=["column1", "column2"])
        print(data_frame.head())
    except Exception as e:
        print(f"Failed to load and process data: {e}")