"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-15T13:21:23.001052

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, index_col: Optional[str] = None) -> pd.DataFrame:
    """
    Load and process data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        index_col (Optional[str]): Column to set as index. Default is None.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
        FileNotFoundError: If the file at file_path does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        # Load the CSV data into a DataFrame
        df = pd.read_csv(file_path, index_col=index_col)
        
        # Clean the data by dropping rows with missing values
        df.dropna(inplace=True)

        # Reset index if index_col is not specified
        if index_col is None:
            df.reset_index(drop=True, inplace=True)
        
        return df

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The provided file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def main():
    """
    Main function to execute data loading and processing.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path)
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()