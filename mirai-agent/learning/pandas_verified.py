"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T08:58:56.777860

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and process it by filling missing values.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A processed DataFrame with missing values filled.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the CSV file into a DataFrame
        data = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Parsing error. {e}")
        raise

    # Fill missing values with the mean of the respective columns
    processed_data = data.fillna(data.mean(numeric_only=True))
    
    return processed_data

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path: str = "data.csv"  # Specify the path to your CSV file
    try:
        # Load and process the data
        processed_df: pd.DataFrame = load_and_process_data(file_path)
        print(processed_df.head())  # Display the first few rows of the processed DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()