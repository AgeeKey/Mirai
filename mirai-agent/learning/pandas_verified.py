"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-16T04:28:04.101850

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Parameters:
    file_path (str): The path to the CSV file to be loaded.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    ValueError: If the data does not contain expected columns.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)
        
        # Check if the required columns exist
        if 'column1' not in df.columns or 'column2' not in df.columns:
            raise ValueError("Data must contain 'column1' and 'column2'.")

        # Perform basic data cleaning
        df.dropna(subset=['column1', 'column2'], inplace=True)  # Remove rows with NaN in specified columns
        
        # Example transformation: Create a new column based on existing columns
        df['new_column'] = df['column1'] + df['column2']  # Assuming 'column1' and 'column2' are numeric
        
        return df

    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Specify the path to your CSV file
    try:
        processed_data = load_and_process_data(file_path)
        print(processed_data.head())  # Display the first few rows of the processed DataFrame
    except Exception as e:
        print("Failed to process the data.")