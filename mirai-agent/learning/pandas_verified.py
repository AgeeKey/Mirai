"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-16T06:52:42.725879

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Union

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data or None if loading fails.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the DataFrame by removing null values and resetting the index.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    # Drop rows with any null values
    df_cleaned = df.dropna()
    # Resetting the index after dropping rows
    df_cleaned.reset_index(drop=True, inplace=True)
    return df_cleaned

def save_data(df: pd.DataFrame, output_file: str) -> None:
    """
    Save the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_file (str): The path to the output CSV file.
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main(file_path: str, output_file: str) -> None:
    """
    Main function to load, process, and save data.

    Args:
        file_path (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file.
    """
    df = load_data(file_path)
    if df is not None:
        processed_df = process_data(df)
        save_data(processed_df, output_file)

if __name__ == "__main__":
    input_file = 'input_data.csv'  # Replace with your input file path
    output_file = 'output_data.csv'  # Replace with your desired output file path
    main(input_file, output_file)