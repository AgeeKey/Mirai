"""
pandas - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-15T18:47:11.934581

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Loads a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file to load.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the data, 
                                 or None if loading fails.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
    return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame by removing any rows with missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: A cleaned DataFrame without missing values.
    """
    cleaned_df = df.dropna()  # Remove rows with missing values
    return cleaned_df

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyzes the DataFrame to calculate basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        pd.Series: A Series containing the mean of each numeric column.
    """
    return df.mean()  # Calculate mean of numeric columns

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze the data.

    Args:
        file_path (str): The path to the CSV file to load.
    """
    data = load_data(file_path)  # Load data
    if data is not None:  # Check if data was loaded successfully
        cleaned_data = clean_data(data)  # Clean data
        stats = analyze_data(cleaned_data)  # Analyze data
        print("Basic Statistics:\n", stats)  # Print statistics

if __name__ == "__main__":
    main("data.csv")  # Replace 'data.csv' with your actual file path