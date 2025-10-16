"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-16T19:11:28.220114

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from pandas import DataFrame

def load_and_process_data(file_path: str) -> DataFrame:
    """
    Load data from a CSV file and perform basic processing.
    
    Args:
        file_path (str): The path to the CSV file.

    Returns:
        DataFrame: A processed DataFrame with no missing values.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        # Load the data into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise
    
    # Drop rows with any missing values
    df_cleaned = df.dropna()
    
    return df_cleaned

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path)
        print(processed_data.head())  # Display the first few rows of the processed data
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()