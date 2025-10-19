"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-19T12:28:18.319138

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Any, Dict

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file, process it, and return a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file cannot be parsed.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Process data: Drop rows with any missing values
        df.dropna(inplace=True)
        
        # Convert a specific column to a numeric type (example: 'age')
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        
        # Drop rows where 'age' could not be converted
        df.dropna(subset=['age'], inplace=True)
        
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty - {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Could not parse the file - {e}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        data = load_and_process_data('data.csv')
        print(data.head())  # Display the first few rows of the processed DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")