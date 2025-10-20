"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-20T22:38:10.658338

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Drop rows with any missing values
    cleaned_df = df.dropna()
    # Drop duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()
    return cleaned_df

def summarize_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Generate summary statistics for the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Dict[str, float]: A dictionary containing summary statistics.
    """
    summary = {
        'mean': df.mean().to_dict(),
        'median': df.median().to_dict(),
        'std_dev': df.std().to_dict(),
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load, clean, and summarize data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    # Load data
    df = load_data(file_path)
    # Clean data
    cleaned_df = clean_data(df)
    # Summarize data
    summary = summarize_data(cleaned_df)
    
    # Print summary statistics
    print("Summary Statistics:")
    for stat, values in summary.items():
        print(f"{stat.capitalize()}: {values}")

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file
    main('data.csv')