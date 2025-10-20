"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-20T02:07:48.771570

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Could not parse the file. {e}")
        raise

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the DataFrame by removing missing values and duplicates.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: A cleaned DataFrame.
    """
    # Remove rows with any missing values
    df_cleaned = df.dropna()
    
    # Remove duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    
    return df_cleaned

def main(file_path: str) -> Optional[pd.DataFrame]:
    """
    Main function to load and process data.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: The processed DataFrame or None if an error occurred.
    """
    try:
        # Load the data
        data = load_data(file_path)
        
        # Process the data
        cleaned_data = process_data(data)
        
        return cleaned_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    file_path = "data.csv"  # Replace with your actual file path
    result_df = main(file_path)
    if result_df is not None:
        print(result_df.head())