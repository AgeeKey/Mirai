"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T20:48:41.156612

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if loading fails.
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
        print("Error: There was a parsing error.")
        return None

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the DataFrame by dropping missing values.

    Args:
        df (pd.DataFrame): The DataFrame to preprocess.

    Returns:
        pd.DataFrame: The preprocessed DataFrame with missing values dropped.
    """
    return df.dropna()

def main(file_path: str) -> None:
    """Main function to load and preprocess data.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        print("Data loaded successfully.")
        print("Original DataFrame:")
        print(df.head())  # Display the first few rows of the original DataFrame
        
        processed_df = preprocess_data(df)  # Preprocess the data
        print("Processed DataFrame (missing values dropped):")
        print(processed_df.head())  # Display the first few rows of the processed DataFrame

if __name__ == "__main__":
    # Example usage: replace 'data.csv' with your actual file path
    main('data.csv')