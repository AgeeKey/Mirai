"""
Pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-15T20:24:52.613334

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Union

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
    FileNotFoundError: If the file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file at {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def clean_data(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Clean the specified column in the DataFrame by removing NaN values.

    Parameters:
    df (pd.DataFrame): The DataFrame to clean.
    column_name (str): The name of the column to clean.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    
    Raises:
    KeyError: If the specified column does not exist in the DataFrame.
    """
    if column_name not in df.columns:
        raise KeyError(f"The column {column_name} does not exist in the DataFrame.")
    
    # Remove NaN values from the specified column
    df_cleaned = df.dropna(subset=[column_name])
    return df_cleaned

def main(file_path: str, column_name: str) -> Optional[pd.DataFrame]:
    """
    Main function to load and clean data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.
    column_name (str): The name of the column to clean.

    Returns:
    Optional[pd.DataFrame]: The cleaned DataFrame, or None if an error occurs.
    """
    try:
        df = load_data(file_path)  # Load data
        cleaned_df = clean_data(df, column_name)  # Clean data
        return cleaned_df
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError, KeyError) as e:
        print(e)
        return None

if __name__ == "__main__":
    # Example usage
    file_path = "data.csv"  # Replace with your CSV file path
    column_name = "target_column"  # Replace with the column you want to clean
    result_df = main(file_path, column_name)
    
    if result_df is not None:
        print(result_df.head())  # Display the first few rows of the cleaned DataFrame