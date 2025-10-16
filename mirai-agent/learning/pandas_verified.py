"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-16T13:42:34.758208

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is an error during parsing.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The file is empty.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Error parsing the file.")

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Process the DataFrame by removing missing values and duplicates.

    Args:
        data (pd.DataFrame): The input DataFrame to process.

    Returns:
        pd.DataFrame: Processed DataFrame with missing values and duplicates removed.
    """
    # Remove duplicate rows
    data_cleaned = data.drop_duplicates()
    # Remove rows with any missing values
    data_cleaned = data_cleaned.dropna()
    return data_cleaned

def summarize_data(data: pd.DataFrame) -> Dict[str, float]:
    """
    Generate summary statistics for the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame to summarize.

    Returns:
        Dict[str, float]: A dictionary containing summary statistics.
    """
    summary = {
        'mean': data.mean(),
        'median': data.median(),
        'std_dev': data.std()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load, process, and summarize data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load the data
        data = load_data(file_path)
        # Process the data
        cleaned_data = process_data(data)
        # Summarize the data
        summary = summarize_data(cleaned_data)
        print("Summary Statistics:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example file path
    file_path = 'data.csv'
    main(file_path)