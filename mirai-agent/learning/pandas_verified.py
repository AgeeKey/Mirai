"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-18T14:30:04.467202

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, List

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a DataFrame.

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
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("No data in file.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def filter_data(df: pd.DataFrame, column: str, value: Optional[str] = None) -> pd.DataFrame:
    """Filter DataFrame based on a specified column and value.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column name to filter on.
        value (Optional[str]): The value to filter for. If None, returns the original DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if value is not None:
        if column in df.columns:
            return df[df[column] == value]
        else:
            raise ValueError(f"Column '{column}' does not exist in DataFrame.")
    return df

def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Save the DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): The output file path for the CSV.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        df.to_csv(output_path, index=False)
    except IOError as e:
        raise IOError(f"Error writing to file: {output_path}") from e

def main(input_file: str, output_file: str, filter_column: str, filter_value: Optional[str]) -> None:
    """Main function to load, filter, and save data.

    Args:
        input_file (str): Path to input CSV file.
        output_file (str): Path to output CSV file.
        filter_column (str): Column name to filter on.
        filter_value (Optional[str]): Value to filter for.
    """
    # Load data from the input file
    data = load_data(input_file)
    
    # Filter the DataFrame
    filtered_data = filter_data(data, filter_column, filter_value)
    
    # Save the filtered DataFrame to the output file
    save_data(filtered_data, output_file)

if __name__ == "__main__":
    input_csv = "input_data.csv"  # Change as required
    output_csv = "filtered_data.csv"  # Change as required
    column_to_filter = "category"  # Change as required
    value_to_filter = "A"  # Change as required

    main(input_csv, output_csv, column_to_filter, value_to_filter)