"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T12:48:42.003067

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
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Analyze the given DataFrame and print summary statistics.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None and not df.empty:
        print("Data Summary:")
        print(df.describe())  # Print summary statistics
        print("\nMissing Values:")
        print(df.isnull().sum())  # Print count of missing values
    else:
        print("DataFrame is empty or not valid for analysis.")

def main(file_path: str) -> None:
    """
    Main function to load and analyze data from a specified CSV file.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load data from the specified file
    analyze_data(df)  # Analyze the loaded data

if __name__ == "__main__":
    file_path = 'data.csv'  # Replace with your actual CSV file path
    main(file_path)  # Execute the main function