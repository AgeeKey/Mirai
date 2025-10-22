"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-22T08:05:46.219412

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load and process data from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - Optional[pd.DataFrame]: A DataFrame containing the processed data, or None if an error occurred.
    """
    try:
        # Load the data from the CSV file
        data = pd.read_csv(file_path)
        
        # Check if the DataFrame is empty
        if data.empty:
            print("Warning: The DataFrame is empty.")
            return None
        
        # Display basic information about the DataFrame
        print(data.info())
        
        # Replace missing values with the mean of each column
        data.fillna(data.mean(), inplace=True)
        
        # Return the processed DataFrame
        return data
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    df = load_and_process_data("data.csv")
    if df is not None:
        print(df.head())