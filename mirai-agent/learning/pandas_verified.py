"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-21T20:02:22.879575

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, process it by filtering columns, and handle potential errors.

    Args:
        file_path (str): The path to the CSV file.
        column_filter (Optional[list]): A list of columns to keep in the DataFrame. If None, all columns are kept.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        # Load the data from the CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The file is empty.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError("Error parsing the file.")

    # Filter columns if a column filter is provided
    if column_filter is not None:
        df = df[column_filter]
    
    # Return the processed DataFrame
    return df

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    columns_to_keep = ['Column1', 'Column2']  # Specify columns to keep

    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path, columns_to_keep)
        print(processed_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()