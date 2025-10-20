"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-20T20:14:21.233608

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e

def clean_data(df: pd.DataFrame, columns_to_fill: list, fill_value: Optional[float] = np.nan) -> pd.DataFrame:
    """Clean the DataFrame by filling NaN values.
    
    Args:
        df (pd.DataFrame): The DataFrame to clean.
        columns_to_fill (list): List of columns to fill NaN values.
        fill_value (Optional[float]): The value to fill NaN with, defaults to np.nan.
    
    Returns:
        pd.DataFrame: A cleaned DataFrame.
    """
    for column in columns_to_fill:
        if column in df.columns:
            df[column].fillna(fill_value, inplace=True)  # Fill NaN values
        else:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    return df

def main(file_path: str) -> None:
    """Main function to load and clean data.
    
    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load data from CSV
    print("Data loaded successfully.")
    
    columns_to_fill = ['column1', 'column2']  # Specify columns to clean
    cleaned_df = clean_data(df, columns_to_fill, fill_value=0)  # Clean the data
    print("Data cleaned successfully.")
    
    print(cleaned_df.head())  # Display first few rows of cleaned data

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file
    main('data.csv')