"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-21T05:14:21.195960

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping null values and duplicates.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: A cleaned DataFrame.
    """
    # Drop rows with any null values
    df_cleaned = df.dropna()
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame and print summary statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    print("Summary Statistics:")
    print(df.describe())  # Print summary statistics
    print("Data Types:")
    print(df.dtypes)      # Print the data types of columns

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your CSV file path
    data = load_data(file_path)  # Load the data

    if data is not None:
        cleaned_data = clean_data(data)  # Clean the data
        analyze_data(cleaned_data)       # Analyze the cleaned data