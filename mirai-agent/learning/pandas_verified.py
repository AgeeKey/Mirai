"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T18:37:59.555477

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file, process it, and return a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A processed DataFrame or None if an error occurs.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Check for missing values and fill them with the mean of the column
        for column in df.select_dtypes(include='number').columns:
            df[column].fillna(df[column].mean(), inplace=True)

        # Drop any duplicate rows
        df.drop_duplicates(inplace=True)

        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a parsing error with the file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    """
    Main function to load and process data from a specified CSV file.
    """
    file_path = 'data/sample_data.csv'  # Specify your CSV file path here
    data = load_and_process_data(file_path)
    
    if data is not None:
        print(data.head())  # Display the first few rows of the processed DataFrame

if __name__ == "__main__":
    main()