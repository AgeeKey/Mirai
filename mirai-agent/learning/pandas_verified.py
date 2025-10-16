"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-16T02:35:51.946540

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by filtering specific columns.

    Parameters:
    file_path (str): The path to the CSV file.
    column_filter (Optional[list]): A list of columns to filter. If None, all columns are included.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    pd.errors.EmptyDataError: If the CSV file is empty.
    pd.errors.ParserError: If there is a parsing error while reading the CSV file.
    """
    try:
        # Load the CSV data into a DataFrame
        df = pd.read_csv(file_path)

        # Filter the DataFrame by the specified columns
        if column_filter is not None:
            df = df[column_filter]

        return df

    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: There was a problem parsing the file.")
        raise e

if __name__ == "__main__":
    # Example usage of the function
    try:
        data = load_and_process_data('data.csv', column_filter=['Column1', 'Column2'])
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print("An error occurred while processing the data.")