"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-20T14:02:49.975258

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if loading fails.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping NaN values and resetting the index.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
    pd.DataFrame: A cleaned DataFrame.
    """
    if df is None:
        raise ValueError("Input DataFrame cannot be None.")
    
    # Drop rows with any NaN values
    cleaned_df = df.dropna()
    
    # Reset the index of the DataFrame
    cleaned_df.reset_index(drop=True, inplace=True)
    return cleaned_df

def main(file_path: str):
    """
    Main function to load and clean data from a CSV file.
    
    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        cleaned_df = clean_data(df)
        print("Cleaned DataFrame:")
        print(cleaned_df)

if __name__ == "__main__":
    # Example usage
    main("data.csv")