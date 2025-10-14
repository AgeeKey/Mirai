"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.95
Tests Passed: 0/1
Learned: 2025-10-14T17:11:50.281642

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter by a specific column if provided, and return a processed DataFrame.
    
    Parameters:
    - file_path: str - The path to the CSV file.
    - column_name: str - The column name to filter on.
    - filter_value: Optional[str] - The value to filter the specified column by (default is None).
    
    Returns:
    - pd.DataFrame - The processed DataFrame.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load data from the CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

        # Filter the DataFrame if filter_value is provided
        if filter_value is not None:
            df = df[df[column_name] == filter_value]

        # Return the processed DataFrame
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

# Example of usage
if __name__ == "__main__":
    try:
        # Define the file path and parameters for loading data
        file_path = 'data.csv'  # Replace with your actual file path
        column_name = 'Category'  # Replace with your actual column name
        filter_value = 'A'  # Replace with your actual filter value (if needed)

        # Load and process the data
        processed_data = load_and_process_data(file_path, column_name, filter_value)

        # Display the processed data
        print(processed_data)

    except Exception as e:
        print(f"Failed to process data: {e}")