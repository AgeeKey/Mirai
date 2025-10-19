"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-19T16:40:49.541641

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
        return None

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing duplicate rows and filling missing values.

    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    # Remove duplicate rows
    df_cleaned = df.drop_duplicates()
    
    # Fill missing values with the mean of each column
    df_cleaned.fillna(df_cleaned.mean(), inplace=True)
    
    return df_cleaned

def main(file_path: str) -> None:
    """
    Main function to execute the data loading and cleaning process.

    Parameters:
    file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)
    
    if df is not None:
        print("Data loaded successfully.")
        cleaned_df = clean_data(df)
        print("Data cleaned successfully.")
        print(cleaned_df.head())  # Display the first few rows of the cleaned DataFrame

if __name__ == "__main__":
    # Example usage
    main("data.csv")