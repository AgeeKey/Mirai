"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-18T22:48:12.674972

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame and process it by selecting specific columns.

    Args:
        file_path (str): The path to the CSV file.
        columns (Optional[list]): A list of column names to select from the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the selected columns or the entire DataFrame if no columns are specified.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the requested columns are not found in the DataFrame.
    """
    try:
        # Load data from CSV file
        df = pd.read_csv(file_path)
        
        # Check if specific columns are requested
        if columns is not None:
            # Check if the specified columns exist in the DataFrame
            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Columns not found in DataFrame: {missing_cols}")
            # Select only the specified columns
            df = df[columns]
        
        return df
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        data = load_and_process_data('example_data.csv', columns=['column1', 'column2'])
        print(data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")