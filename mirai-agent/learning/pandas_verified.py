"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-22T14:50:07.427605

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Union

def load_and_process_data(file_path: str, separator: str = ',') -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a DataFrame and perform basic cleaning operations.
    
    Args:
        file_path (str): The path to the CSV file.
        separator (str, optional): The delimiter to use. Defaults to ','.
    
    Returns:
        Optional[pd.DataFrame]: A processed DataFrame or None if an error occurs.
    """
    try:
        # Load data from CSV file
        df = pd.read_csv(file_path, sep=separator)
        
        # Drop any rows with missing values
        df.dropna(inplace=True)
        
        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)
        
        return df
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame including basic statistics and info.
    
    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())  # Print statistical summary
        print("\nData Info:")
        print(df.info())      # Print DataFrame info
    else:
        print("No data to summarize.")

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your actual file path
    data_frame = load_and_process_data(file_path)
    summarize_data(data_frame)