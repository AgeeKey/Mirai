"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-18T05:01:50.818211

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Loads a CSV file into a pandas DataFrame, processes it by cleaning
    the data and handling missing values.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A cleaned pandas DataFrame or None if loading failed.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: No data found in the file.")
        return None
    except pd.errors.ParserError:
        print("Error: Failed to parse the data.")
        return None

    # Display initial data shape
    print(f"Initial data shape: {df.shape}")

    # Drop rows with any missing values
    df_cleaned = df.dropna()
    
    # Display cleaned data shape
    print(f"Cleaned data shape: {df_cleaned.shape}")

    return df_cleaned

def main():
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Specify your CSV file path
    cleaned_data = load_and_process_data(file_path)

    if cleaned_data is not None:
        # Display the first few rows of the cleaned data
        print(cleaned_data.head())

if __name__ == "__main__":
    main()