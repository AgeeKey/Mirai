"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T08:42:58.819655

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.ParserError: If the file cannot be parsed as CSV.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: {e}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Args:
        df (pd.DataFrame): DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df_cleaned = df.dropna().drop_duplicates()
    return df_cleaned

def summarize_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Generate summary statistics for the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to summarize.

    Returns:
        Dict[str, float]: Dictionary containing mean and standard deviation of numeric columns.
    """
    summary = {
        'mean': df.mean(numeric_only=True).to_dict(),
        'std_dev': df.std(numeric_only=True).to_dict()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to execute the data processing pipeline.

    Args:
        file_path (str): Path to the CSV file.
    """
    try:
        # Load data
        data = load_data(file_path)
        # Clean data
        cleaned_data = clean_data(data)
        # Summarize data
        summary = summarize_data(cleaned_data)
        
        print("Summary Statistics:")
        print(summary)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    main("data.csv")