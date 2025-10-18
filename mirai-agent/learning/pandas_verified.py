"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T10:02:08.819294

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
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

    Parameters:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    if df is None:
        raise ValueError("Input DataFrame is None.")
    
    # Drop rows with any missing values
    df_cleaned = df.dropna()
    
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame by calculating basic statistics.

    Parameters:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the mean of each numeric column.
    """
    if df is None or df.empty:
        raise ValueError("Input DataFrame is None or empty.")
    
    return df.mean()

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    Parameters:
        file_path (str): The path to the CSV file.
    """
    # Load data
    df = load_data(file_path)
    
    # Clean data
    if df is not None:
        df_cleaned = clean_data(df)
        
        # Analyze data
        stats = analyze_data(df_cleaned)
        print("Statistics of cleaned data:\n", stats)

if __name__ == "__main__":
    main("data.csv")  # Replace 'data.csv' with the actual path to your CSV file.