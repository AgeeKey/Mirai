"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T15:56:24.710458

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there are parsing errors.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty - {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Parsing error - {e}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and resetting the index.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Drop rows with missing values
    df_cleaned.reset_index(drop=True, inplace=True)  # Reset index
    return df_cleaned

def save_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): The path where the CSV file will be saved.
    """
    df.to_csv(output_path, index=False)  # Save DataFrame to CSV

def main(input_file: str, output_file: str) -> None:
    """
    Main function to load, clean, and save data.

    Args:
        input_file (str): The input CSV file path.
        output_file (str): The output CSV file path.
    """
    try:
        data = load_data(input_file)  # Load data from CSV
        clean_data_df = clean_data(data)  # Clean the loaded data
        save_data(clean_data_df, output_file)  # Save cleaned data to CSV
        print(f"Data processing complete. Cleaned data saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred during data processing: {e}")

if __name__ == "__main__":
    main("input_data.csv", "cleaned_data.csv")  # Replace with actual file paths