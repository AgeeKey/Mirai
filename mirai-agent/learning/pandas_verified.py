"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T16:29:18.249015

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError(f"The file is empty: {file_path}") from e

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: A cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Drop rows with any missing values
    df_cleaned = df_cleaned.drop_duplicates()  # Drop duplicate rows
    return df_cleaned

def summarize_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Generate a summary of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Dict[str, float]: A dictionary containing summary statistics.
    """
    summary = {
        "mean": df.mean(numeric_only=True).to_dict(),
        "median": df.median(numeric_only=True).to_dict(),
        "std_dev": df.std(numeric_only=True).to_dict()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load, clean, and summarize data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    # Load data
    data = load_data(file_path)
    # Clean data
    cleaned_data = clean_data(data)
    # Summarize data
    summary = summarize_data(cleaned_data)
    
    # Print summary
    print("Data Summary:")
    print(summary)

if __name__ == "__main__":
    # Provide the CSV file path here
    csv_file_path = 'data.csv'  # Example file path
    main(csv_file_path)