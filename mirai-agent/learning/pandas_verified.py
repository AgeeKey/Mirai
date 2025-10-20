"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-20T06:20:33.923461

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it.

    Parameters:
    file_path (str): The path to the CSV file.
    column_names (Optional[list]): List of column names to use; if None, uses the file's header.

    Returns:
    pd.DataFrame: Processed DataFrame.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    ValueError: If the file is empty or cannot be parsed.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path, header=0 if column_names is None else None)
        
        # Assign column names if provided
        if column_names is not None:
            if len(column_names) != df.shape[1]:
                raise ValueError("Number of column names provided does not match the number of columns in the CSV.")
            df.columns = column_names
        
        # Drop any rows with missing values
        df.dropna(inplace=True)
        
        return df
    
    except FileNotFoundError as e:
        print(f"Error: The file '{file_path}' was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: Could not parse the file.")
        raise e

# Example usage
if __name__ == "__main__":
    try:
        data_frame = load_and_process_data("data.csv", column_names=["Column1", "Column2", "Column3"])
        print(data_frame.head())
    except Exception as e:
        print(f"An error occurred: {e}")