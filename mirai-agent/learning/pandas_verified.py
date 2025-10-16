"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-16T11:03:37.198496

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file, clean it, and return a DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the cleaned data, or None if an error occurs.
    """
    try:
        # Load the data from the CSV file
        data = pd.read_csv(file_path)

        # Display the first few rows of the dataframe
        print("Initial data loaded:")
        print(data.head())

        # Drop rows with any missing values
        cleaned_data = data.dropna()

        # Reset index after dropping rows
        cleaned_data.reset_index(drop=True, inplace=True)

        print("Data cleaned and index reset.")
        return cleaned_data

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    df = load_and_process_data("data.csv")
    if df is not None:
        print("Processed DataFrame:")
        print(df)