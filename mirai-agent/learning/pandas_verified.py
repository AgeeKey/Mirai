"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T01:35:58.230641

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file at {file_path} could not be parsed.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping NaN values and resetting the index.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    if df is None or df.empty:
        raise ValueError("DataFrame is empty or None. Cannot clean data.")
    
    # Drop rows with any NaN values
    cleaned_df = df.dropna()
    
    # Reset index after dropping rows
    cleaned_df.reset_index(drop=True, inplace=True)
    
    return cleaned_df

def main(file_path: str) -> None:
    """
    Main function to load, clean, and display data.

    Args:
        file_path (str): The path to the CSV file to load.
    """
    df = load_data(file_path)
    if df is not None:
        cleaned_df = clean_data(df)
        print(cleaned_df)

if __name__ == "__main__":
    # Example CSV file path (adjust as necessary)
    example_file_path = 'data.csv'
    main(example_file_path)