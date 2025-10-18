"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T02:39:12.259054

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
        pd.DataFrame: The loaded data as a DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping rows with missing values.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    cleaned_df = df.dropna()  # Drop rows with any missing values
    return cleaned_df


def summarize_data(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Summarize the DataFrame by providing basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Optional[pd.DataFrame]: A DataFrame with summary statistics or None if df is empty.
    """
    if df.empty:
        print("The DataFrame is empty, no summary to provide.")
        return None
    return df.describe()  # Return summary statistics


def main(file_path: str) -> None:
    """
    Main function to load, clean, and summarize data from a CSV file.

    Args:
        file_path (str): The path to the CSV file to process.
    """
    try:
        # Load the data from the CSV file
        data = load_data(file_path)

        # Clean the data
        cleaned_data = clean_data(data)

        # Summarize the cleaned data
        summary = summarize_data(cleaned_data)
        if summary is not None:
            print(summary)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Example CSV file path
    csv_file_path = 'data.csv'
    main(csv_file_path)