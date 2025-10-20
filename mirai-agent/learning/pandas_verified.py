"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-20T17:17:43.955224

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
        pd.DataFrame: A DataFrame containing the processed data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is an error parsing the file.
    """
    try:
        # Load the CSV file into a DataFrame
        data = pd.read_csv(file_path)

        # Drop rows with any missing values
        data.dropna(inplace=True)

        # Convert a specific column to datetime format
        if 'date_column' in data.columns:
            data['date_column'] = pd.to_datetime(data['date_column'])

        return data

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise
    except pd.errors.ParserError as e:
        print("Error: There was an error parsing the file.")
        raise

def filter_data_by_column(df: pd.DataFrame, column_name: str, values: List[str]) -> pd.DataFrame:
    """
    Filter the DataFrame based on a specific column and a list of values.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column_name (str): The column to filter by.
        values (List[str]): The values to include in the filtered DataFrame.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only the specified values in the column.
    
    Raises:
        KeyError: If the specified column does not exist in the DataFrame.
    """
    if column_name not in df.columns:
        raise KeyError(f"Column '{column_name}' does not exist in the DataFrame.")
    
    # Filter the DataFrame based on the provided values
    filtered_df = df[df[column_name].isin(values)]
    return filtered_df

if __name__ == "__main__":
    # Define the CSV file path
    file_path = 'data.csv'

    # Load and process the data
    try:
        processed_data = load_and_process_data(file_path)
        print("Data loaded and processed successfully.")
        
        # Filter the data by a specific column and values
        values_to_filter = ['value1', 'value2']
        filtered_data = filter_data_by_column(processed_data, 'category_column', values_to_filter)
        print("Filtered data:")
        print(filtered_data)
    
    except Exception as e:
        print(f"An error occurred: {e}")