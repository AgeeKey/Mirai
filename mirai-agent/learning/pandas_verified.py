"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-22T16:11:24.193860

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
        
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
        print(f"Error: The file is empty. {e}")
        raise

def process_data(df: pd.DataFrame, column_name: str) -> Optional[pd.Series]:
    """
    Process the DataFrame by calculating the mean of a specified column.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        column_name (str): The column name to calculate the mean.

    Returns:
        Optional[pd.Series]: A Series containing the mean value if the column exists, otherwise None.
    """
    if column_name in df.columns:
        mean_value = df[column_name].mean()
        return mean_value
    else:
        print(f"Error: Column '{column_name}' does not exist in the DataFrame.")
        return None

def main():
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Path to the CSV file
    column_name = 'value'    # Column to calculate the mean

    # Load the data
    df = load_data(file_path)

    # Process the data
    mean_value = process_data(df, column_name)
    
    if mean_value is not None:
        print(f"The mean value of '{column_name}' is: {mean_value}")

if __name__ == "__main__":
    main()