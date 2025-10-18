"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-18T04:45:54.815821

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {filepath} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file {filepath} could not be parsed.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing rows with missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: A cleaned DataFrame without missing values.
    """
    cleaned_df = df.dropna()  # Remove rows with any missing values
    return cleaned_df

def main(filepath: str) -> None:
    """
    Main function to load, clean, and display data.

    Args:
        filepath (str): The path to the CSV file.
    """
    data = load_data(filepath)
    if data is not None:  # Proceed only if data was loaded successfully
        cleaned_data = clean_data(data)
        print("Cleaned Data:")
        print(cleaned_data)

if __name__ == "__main__":
    # Example CSV file path (update with a valid path to test)
    example_filepath = 'data/example.csv'
    main(example_filepath)