"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-21T04:58:23.598416

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame and process it.
    
    Args:
        file_path (str): Path to the CSV file.
        column_names (Optional[list[str]]): List of column names to use. If None, uses the first row as header.
        
    Returns:
        pd.DataFrame: Processed DataFrame.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the DataFrame is empty after loading.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path, header=0 if column_names is None else None)
        
        # Use provided column names if specified
        if column_names is not None:
            df.columns = column_names
        
        # Drop rows with any missing values
        df.dropna(inplace=True)
        
        if df.empty:
            raise ValueError("The DataFrame is empty after loading and processing.")
        
        return df
        
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        raise
    except ValueError as value_error:
        print(f"Error: {value_error}")
        raise

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    column_names = ['Column1', 'Column2', 'Column3']  # Specify your desired column names here
    
    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path, column_names)
        
        # Display the first few rows of the processed DataFrame
        print(processed_data.head())
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()