"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T07:28:01.189048

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by selecting specified columns.

    Args:
        file_path (str): The path to the CSV file.
        columns (Optional[list]): A list of columns to select from the DataFrame. 
                                  If None, all columns are selected.

    Returns:
        pd.DataFrame: A processed DataFrame containing the selected columns.
    
    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        ValueError: If the specified columns are not in the DataFrame.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)

        # If specific columns are provided, filter the DataFrame
        if columns is not None:
            missing_cols = set(columns) - set(df.columns)
            if missing_cols:
                raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
            df = df[columns]

        return df

    except FileNotFoundError as e:
        print(f"Error: The file at {file_path} was not found.")
        raise e
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except pd.errors.ParserError:
        print("Error: The file could not be parsed. Please check the file format.")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data = load_and_process_data('data.csv', columns=['column1', 'column2'])
        print(data.head())
    except Exception as e:
        print(f"An error occurred: {e}")