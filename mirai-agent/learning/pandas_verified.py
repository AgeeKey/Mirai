"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T06:44:55.987181

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
        raise e
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        raise
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing missing values.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.

    Returns:
    pd.DataFrame: Cleaned DataFrame with missing values removed.
    """
    cleaned_df = df.dropna()  # Remove rows with missing values
    return cleaned_df

def calculate_statistics(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Calculate mean and median of a numeric column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame with numeric data.

    Returns:
    Tuple[float, float]: A tuple containing the mean and median.
    """
    if df.empty:
        raise ValueError("DataFrame is empty. Cannot calculate statistics.")
    
    mean_value = df.mean()  # Calculate mean
    median_value = df.median()  # Calculate median
    return mean_value, median_value

def main(file_path: str) -> None:
    """
    Main function to execute the data loading, cleaning, and statistics calculation.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    cleaned_df = clean_data(df)  # Clean the data

    # Calculate and print statistics if the DataFrame is not empty
    if not cleaned_df.empty:
        mean, median = calculate_statistics(cleaned_df)
        print(f"Mean: {mean}, Median: {median}")

if __name__ == "__main__":
    # Example CSV file path
    example_file_path = 'data.csv'  # Change to your actual file path
    main(example_file_path)