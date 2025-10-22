"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-22T19:18:27.945237

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame and process it.

    Parameters:
        file_path (str): The path to the CSV file.
        column_names (Optional[list]): A list of column names to assign to the DataFrame.

    Returns:
        pd.DataFrame: Processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the DataFrame is empty after loading.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Assign custom column names if provided
        if column_names is not None:
            df.columns = column_names
        
        # Check if the DataFrame is empty
        if df.empty:
            raise ValueError("The DataFrame is empty after loading the data.")
        
        # Return the processed DataFrame
        return df

    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found. Please check the path.")
        raise e
    except ValueError as e:
        print(f"Error: {e}")
        raise e

def main():
    # Example usage of the load_and_process_data function
    try:
        df = load_and_process_data('data.csv', column_names=['Column1', 'Column2', 'Column3'])
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()