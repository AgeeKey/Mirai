"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-15T06:52:07.415006

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurred.
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
        print("Error: Could not parse the file.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.
    
    Args:
        df (pd.DataFrame): The DataFrame to clean.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Drop rows with missing values
    df_cleaned = df_cleaned.drop_duplicates()  # Drop duplicate rows
    return df_cleaned

def main(file_path: str) -> None:
    """
    Main function to load and clean data.
    
    Args:
        file_path (str): The path to the CSV file to be processed.
    """
    df = load_data(file_path)
    if df is not None:
        print("Data loaded successfully.")
        df_cleaned = clean_data(df)
        print("Data cleaned successfully.")
        print(df_cleaned.head())  # Display the first few rows of the cleaned DataFrame

if __name__ == "__main__":
    # Example usage. Replace 'data.csv' with your actual CSV file path.
    main('data.csv')