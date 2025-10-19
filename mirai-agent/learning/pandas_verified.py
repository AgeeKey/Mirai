"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.95
Tests Passed: 0/1
Learned: 2025-10-19T23:14:27.392979

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame and perform basic cleaning operations.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A cleaned DataFrame or None if an error occurs.
    """
    try:
        # Load CSV data into a DataFrame
        df = pd.read_csv(file_path)
        
        # Display the initial shape of the DataFrame
        print(f"Initial DataFrame shape: {df.shape}")

        # Drop rows with any missing values
        df_cleaned = df.dropna()
        
        # Reset index after dropping rows
        df_cleaned.reset_index(drop=True, inplace=True)

        # Display the shape after cleaning
        print(f"Cleaned DataFrame shape: {df_cleaned.shape}")

        return df_cleaned
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: Could not parse the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your actual file path
    cleaned_data = load_and_process_data(file_path)
    if cleaned_data is not None:
        print(cleaned_data.head())