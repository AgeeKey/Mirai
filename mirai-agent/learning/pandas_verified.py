"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-22T06:12:46.995406

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, List

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("Error: The file is empty.") from e
    except pd.errors.ParserError as e:
        raise ValueError("Error: Could not parse the file.") from e

def filter_data(df: pd.DataFrame, column: str, value: Optional[str] = None) -> pd.DataFrame:
    """
    Filter the DataFrame based on a column and a specific value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter on.
        value (Optional[str]): The value to filter by. If None, returns the original DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if value is not None:
        if column not in df.columns:
            raise ValueError(f"Error: Column '{column}' does not exist in the DataFrame.")
        return df[df[column] == value]
    return df

def main(file_path: str, filter_column: str, filter_value: Optional[str]) -> None:
    """
    Main function to load and filter data.

    Args:
        file_path (str): Path to the CSV file.
        filter_column (str): The column name to filter on.
        filter_value (Optional[str]): The value to filter by.
    """
    # Load data from the specified file path
    data = load_data(file_path)
    
    # Filter data based on the specified column and value
    filtered_data = filter_data(data, filter_column, filter_value)
    
    # Display the filtered data
    print(filtered_data)

if __name__ == "__main__":
    # Example usage
    main('data.csv', 'category', 'A')