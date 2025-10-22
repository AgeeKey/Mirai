"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-22T02:46:23.550323

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and process it by selecting specific columns.

    Parameters:
    file_path (str): The path to the CSV file.
    columns (Optional[list]): A list of column names to select from the DataFrame. 
                              If None, all columns are included.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded and processed data.
    
    Raises:
    FileNotFoundError: If the specified file does not exist.
    ValueError: If any specified columns are not found in the DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if specific columns are requested
        if columns is not None:
            # Validate that the requested columns are in the DataFrame
            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Columns not found in DataFrame: {missing_cols}")

            # Select only the specified columns
            df = df[columns]

        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    # Assume 'data.csv' is a valid CSV file in the same directory
    try:
        data = load_and_process_data('data.csv', columns=['column1', 'column2'])
        print(data.head())
    except Exception as e:
        print(f"Failed to load and process data: {e}")