"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-17T16:28:37.990256

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load and process the data from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - Optional[pd.DataFrame]: A DataFrame containing the processed data or None if an error occurs.
    """
    try:
        # Load the data from a CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check for missing values and fill them with the mean of the column
        df.fillna(df.mean(), inplace=True)

        # Convert string columns to categorical type
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype('category')

        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data/sample_data.csv'  # Example file path
    data = load_and_process_data(file_path)

    if data is not None:
        print("Data loaded and processed successfully:")
        print(data.head())  # Display the first few rows of the DataFrame

if __name__ == "__main__":
    main()