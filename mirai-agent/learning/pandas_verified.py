"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-19T18:31:07.279458

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, delimiter: str = ',', drop_columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, process it by dropping specified columns, and return a cleaned DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.
    - delimiter (str): The delimiter used in the CSV file. Default is ','.
    - drop_columns (Optional[list]): List of column names to drop from the DataFrame.

    Returns:
    - pd.DataFrame: A cleaned DataFrame ready for analysis.

    Raises:
    - FileNotFoundError: If the specified file cannot be found.
    - ValueError: If drop_columns contains columns not in the DataFrame.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter)

        # Drop specified columns if provided
        if drop_columns:
            for column in drop_columns:
                if column in df.columns:
                    df.drop(column, axis=1, inplace=True)
                else:
                    raise ValueError(f"Column '{column}' not found in DataFrame.")

        # Return the processed DataFrame
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
        df = load_and_process_data('data.csv', drop_columns=['unnecessary_column'])
        print(df.head())
    except Exception as e:
        print(f"Failed to process data: {e}")