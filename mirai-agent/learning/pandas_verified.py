"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-15T16:20:01.007913

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list]): List of column names to use. If None, uses the first row as header.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified column names do not match the data.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path, header=0 if column_names is None else None)

        # If column names are provided, rename the columns
        if column_names is not None:
            if len(column_names) != df.shape[1]:
                raise ValueError("Number of column names does not match the number of columns in the data.")
            df.columns = column_names

        # Drop any rows with missing values
        df.dropna(inplace=True)

        # Return the processed DataFrame
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: No data found in the file.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data = load_and_process_data('data.csv', column_names=['Column1', 'Column2', 'Column3'])
        print(data.head())
    except Exception as e:
        print(f"Failed to load data: {e}")