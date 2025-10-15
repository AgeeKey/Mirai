"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T00:13:49.655261

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and perform basic data processing.
    
    Parameters:
        file_path (str): The path to the CSV file.
        index_col (Optional[str]): The column to be used as the row labels of the DataFrame.
        
    Returns:
        pd.DataFrame: A processed DataFrame.
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path, index_col=index_col)
        
        # Drop any rows with missing values
        df.dropna(inplace=True)
        
        # Reset index if no index column is specified
        if index_col is None:
            df.reset_index(drop=True, inplace=True)
        
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: There was an issue parsing the file. {e}")
        raise

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data/sample_data.csv'  # Path to your CSV file
    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path)
        print(processed_data.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()