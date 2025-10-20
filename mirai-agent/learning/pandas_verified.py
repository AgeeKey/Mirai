"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T12:41:29.654920

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Union

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
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
        print("Error: The file could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("Basic Data Analysis:")
        print(f"Shape of the DataFrame: {df.shape}")
        print("Data Types:")
        print(df.dtypes)
        print("Summary Statistics:")
        print(df.describe())
    else:
        print("No data to analyze.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data.

    Parameters:
    file_path (str): The path to the CSV file to be loaded.
    """
    df = load_data(file_path)  # Load the data
    analyze_data(df)           # Analyze the loaded data

if __name__ == "__main__":
    # Example usage
    main("example_data.csv")  # Replace with your actual CSV file path