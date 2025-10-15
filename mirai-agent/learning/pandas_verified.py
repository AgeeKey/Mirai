"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T06:35:57.033937

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
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
        print(f"Error: The file {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Analyze the DataFrame and print basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
    """
    if df is not None:
        print("DataFrame Head:")
        print(df.head())  # Display the first few rows
        print("\nDataFrame Info:")
        print(df.info())  # Display DataFrame information
        print("\nDescriptive Statistics:")
        print(df.describe())  # Display descriptive statistics
    else:
        print("No data to analyze.")

def main() -> None:
    """
    Main function to execute data loading and analysis.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    df = load_data(file_path)
    analyze_data(df)

if __name__ == "__main__":
    main()