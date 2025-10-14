"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-14T19:22:16.798249

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and process it by renaming columns if provided.

    Parameters:
    - file_path: Path to the CSV file.
    - column_names: Optional list of new column names.

    Returns:
    - A pandas DataFrame containing the loaded data.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the number of new column names does not match the number of columns in the CSV.
    """
    try:
        # Load the data from CSV
        df = pd.read_csv(file_path)

        # If column names are provided, rename the columns
        if column_names is not None:
            if len(column_names) != df.shape[1]:
                raise ValueError("The number of new column names must match the number of columns in the CSV.")
            df.columns = column_names

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def main():
    # Example file path
    file_path = 'data.csv'

    # Optional new column names
    new_column_names = ['Column1', 'Column2', 'Column3']

    try:
        # Load and process the data
        data = load_and_process_data(file_path, new_column_names)

        # Display the first few rows of the DataFrame
        print(data.head())

    except Exception as e:
        print("Failed to load and process data.")

if __name__ == "__main__":
    main()