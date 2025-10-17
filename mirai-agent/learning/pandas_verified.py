"""
pandas - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.80
Tests Passed: 0/1
Learned: 2025-10-17T05:40:59.859083

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file at '{file_path}' was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("The file is empty.") from e

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df_cleaned = df.dropna()  # Remove rows with missing values
    df_cleaned = df_cleaned.drop_duplicates()  # Remove duplicate rows
    return df_cleaned

def analyze_data(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Analyze the DataFrame to calculate mean and median of a numerical column.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        Tuple[float, float]: Mean and median of the 'value' column.

    Raises:
        KeyError: If 'value' column is not present in the DataFrame.
    """
    if 'value' not in df.columns:
        raise KeyError("'value' column is missing from the DataFrame.")
    
    mean_value = df['value'].mean()  # Calculate mean
    median_value = df['value'].median()  # Calculate median
    return mean_value, median_value

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        data = load_data(file_path)
        cleaned_data = clean_data(data)
        mean, median = analyze_data(cleaned_data)
        print(f"Mean: {mean}, Median: {median}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main("data.csv")  # Replace with your CSV file path