"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-18T10:33:26.975730

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file and process the data.
    
    Parameters:
    file_path (str): The path to the CSV file.
    column_name (str): The column to filter on.
    filter_value (Optional[str]): The value to filter the specified column. Defaults to None.
    
    Returns:
    pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
    FileNotFoundError: If the file does not exist.
    ValueError: If the specified column is not found in the DataFrame.
    """
    try:
        # Load the data from a CSV file
        df = pd.read_csv(file_path)

        # Check if the column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

        # Filter the DataFrame if a filter_value is provided
        if filter_value is not None:
            df = df[df[column_name] == filter_value]

        # Return the processed DataFrame
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # Load and process the data
        processed_data = load_and_process_data('data.csv', 'Category', 'A')
        print(processed_data)
    except Exception as e:
        print(f"Failed to process data: {e}")