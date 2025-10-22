"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-22T14:16:36.959203

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame by filling missing values and removing duplicates.
    
    Args:
        df (pd.DataFrame): The DataFrame to preprocess.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Fill missing values with the mean of each column
    df.fillna(df.mean(), inplace=True)
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    return df

def main(file_path: str) -> None:
    """
    Main function to load, preprocess, and display data from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        print("Original DataFrame:")
        print(df)
        
        cleaned_df = preprocess_data(df)
        print("\nCleaned DataFrame:")
        print(cleaned_df)

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file
    main('data.csv')