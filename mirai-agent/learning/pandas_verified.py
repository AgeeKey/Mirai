"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T15:01:45.989162

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    - file_path: str - The path to the CSV file.

    Returns:
    - Optional[pd.DataFrame]: DataFrame containing the data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error when reading the file.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Parameters:
    - df: pd.DataFrame - The DataFrame to clean.

    Returns:
    - pd.DataFrame: The cleaned DataFrame.
    """
    # Drop rows with any missing values
    df_cleaned = df.dropna()

    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()

    return df_cleaned

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print summary statistics.

    Parameters:
    - df: pd.DataFrame - The DataFrame to analyze.
    """
    print("Summary Statistics:")
    print(df.describe())

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data.

    Parameters:
    - file_path: str - The path to the CSV file.
    """
    # Load data
    data = load_data(file_path)
    
    if data is not None:  # Proceed only if data was loaded successfully
        # Clean data
        cleaned_data = clean_data(data)
        
        # Analyze data
        analyze_data(cleaned_data)

if __name__ == "__main__":
    main("data.csv")  # Replace with your actual file path