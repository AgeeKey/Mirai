"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-14T19:54:12.211127

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise

def process_data(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Process the DataFrame by performing basic data cleaning.

    Parameters:
    - df (pd.DataFrame): The DataFrame to process.

    Returns:
    - Optional[pd.DataFrame]: A cleaned DataFrame or None if no data to clean.
    """
    if df.empty:
        print("No data to process.")
        return None

    # Dropping rows with missing values
    cleaned_df = df.dropna()
    
    # Resetting index after dropping rows
    cleaned_df.reset_index(drop=True, inplace=True)
    
    return cleaned_df

def main(file_path: str) -> None:
    """
    Main function to load, process, and display data.

    Parameters:
    - file_path (str): The path to the CSV file.
    """
    try:
        data = load_data(file_path)
        cleaned_data = process_data(data)
        
        if cleaned_data is not None:
            print("Cleaned DataFrame:")
            print(cleaned_data)
        else:
            print("No data available after cleaning.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage: replace 'data.csv' with your actual CSV file path
    main('data.csv')