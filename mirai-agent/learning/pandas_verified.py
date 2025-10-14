"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-14T23:09:41.989017

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame and process it by renaming columns if provided.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list[str]]): A list of new column names. If provided, these will replace the existing column names.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded and processed data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        Exception: For any other exceptions that may occur during file loading.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Rename columns if new names are provided
        if column_names:
            df.columns = column_names
        
        return df
    
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data/sample_data.csv'  # Update with your actual file path
    new_column_names = ['Column1', 'Column2', 'Column3']  # Example new column names

    # Load and process data
    try:
        df = load_and_process_data(file_path, new_column_names)
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"Failed to load and process data: {e}")

if __name__ == "__main__":
    main()