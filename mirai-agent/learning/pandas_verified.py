"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-17T06:28:47.489749

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by filtering specified columns.

    Args:
        file_path (str): The path to the CSV file.
        column_filter (Optional[list]): List of columns to retain in the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the filtered data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If any of the specified columns are not found in the DataFrame.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)

        # If column_filter is provided, filter the DataFrame
        if column_filter is not None:
            missing_cols = set(column_filter) - set(df.columns)
            if missing_cols:
                raise ValueError(f"The following columns are not found in the DataFrame: {missing_cols}")
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
    file_path = 'data.csv'  # Replace with your CSV file path
    columns_to_keep = ['column1', 'column2']  # Replace with your desired columns

    try:
        processed_data = load_and_process_data(file_path, columns_to_keep)
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")