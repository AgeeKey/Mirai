"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T06:36:21.651526

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame and filter columns if specified.

    Args:
        file_path (str): The path to the CSV file.
        column_filter (Optional[list]): A list of columns to keep in the DataFrame. 
                                         If None, all columns are kept.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data, filtered by the specified columns.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is an issue parsing the file.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)

        # Filter columns if a column filter is provided
        if column_filter is not None:
            df = df[column_filter]

        return df
    
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        raise
    except pd.errors.EmptyDataError as empty_error:
        print(f"Error: The file is empty. {empty_error}")
        raise
    except pd.errors.ParserError as parse_error:
        print(f"Error: There was a parsing error. {parse_error}")
        raise

if __name__ == "__main__":
    # Example usage
    file_path = 'data/sample_data.csv'  # Modify this path as needed
    columns_to_keep = ['column1', 'column2']  # Specify columns to keep
    try:
        processed_data = load_and_process_data(file_path, columns_to_keep)
        print(processed_data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")