"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-14T15:16:16.692728

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A processed DataFrame.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the CSV data into a DataFrame
        df = pd.read_csv(file_path)

        # Drop rows with any missing values
        df.dropna(inplace=True)

        # Reset index after dropping rows
        df.reset_index(drop=True, inplace=True)

        return df
    except FileNotFoundError as e:
        print(f"Error: The file {file_path} was not found.")
        raise e
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise e
    except pd.errors.ParserError as e:
        print("Error: There was a problem parsing the file.")
        raise e

def calculate_statistics(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Calculate basic statistics for specified columns in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        columns (List[str]): The list of column names to calculate statistics for.

    Returns:
        pd.DataFrame: A DataFrame containing the statistics.
    """
    stats = {}
    for column in columns:
        if column in df.columns:
            stats[column] = {
                'mean': df[column].mean(),
                'std': df[column].std(),
                'min': df[column].min(),
                'max': df[column].max()
            }
        else:
            print(f"Warning: Column '{column}' not found in DataFrame.")
    
    # Convert the statistics dictionary to a DataFrame
    return pd.DataFrame(stats)

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Specify the path to your CSV file
    try:
        data = load_and_process_data(file_path)
        print("Data loaded successfully.")
        
        # Specify the columns for which to calculate statistics
        columns_to_analyze = ['column1', 'column2']  # Replace with actual column names
        stats = calculate_statistics(data, columns_to_analyze)
        
        print("Calculated statistics:")
        print(stats)
    except Exception as e:
        print(f"An error occurred: {e}")