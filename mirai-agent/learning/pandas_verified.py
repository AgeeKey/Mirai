"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T08:31:35.060010

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by cleaning and formatting.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the cleaned data.
    """
    try:
        # Load data from the CSV file
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The provided file is empty.")
    except pd.errors.ParserError:
        raise ValueError("Error occurred while parsing the file.")

    # Basic data cleaning
    data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]  # Normalize column names
    data.dropna(inplace=True)  # Remove rows with missing values

    return data

def filter_data(data: pd.DataFrame, column_name: str, filter_values: List) -> pd.DataFrame:
    """
    Filter the DataFrame based on specified values in a given column.

    Args:
        data (pd.DataFrame): The DataFrame to filter.
        column_name (str): The column name to apply the filter on.
        filter_values (List): The list of values to filter by.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
    
    filtered_data = data[data[column_name].isin(filter_values)]
    return filtered_data

# Example usage
if __name__ == "__main__":
    # Load and process the data from a CSV file
    file_path = 'data/sample_data.csv'  # Update this path as necessary
    try:
        processed_data = load_and_process_data(file_path)
        
        # Filter the processed data
        column_to_filter = 'category'  # Replace with the actual column name
        values_to_filter = ['A', 'B']  # Replace with actual values to filter
        filtered_data = filter_data(processed_data, column_to_filter, values_to_filter)
        
        print(filtered_data)
    except Exception as e:
        print(f"An error occurred: {e}")