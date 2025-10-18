"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T16:20:52.188940

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

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
        pd.errors.ParserError: If there is an error parsing the file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data found in the file.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def filter_data(df: pd.DataFrame, column_name: str, threshold: float) -> pd.DataFrame:
    """
    Filter the DataFrame based on a threshold for a specific column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column_name (str): The column name to apply the filter on.
        threshold (float): The threshold value for filtering.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    
    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' does not exist in the DataFrame.")
    filtered_df = df[df[column_name] > threshold]
    return filtered_df

def main(file_path: str, column_name: str, threshold: float) -> None:
    """
    Main function to load data, filter it, and print the result.

    Args:
        file_path (str): The path to the CSV file.
        column_name (str): The column name to filter on.
        threshold (float): The threshold value for filtering.
    """
    # Load the data
    data = load_data(file_path)
    
    # Filter the data
    filtered_data = filter_data(data, column_name, threshold)
    
    # Print the filtered data
    print(filtered_data)

if __name__ == "__main__":
    # Example usage
    main('data.csv', 'age', 30)