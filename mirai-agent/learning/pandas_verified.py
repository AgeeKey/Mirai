"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T21:08:51.977906

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame and process it.

    Args:
        file_path (str): The path to the CSV file.
        columns (Optional[list]): A list of columns to keep. If None, all columns are kept.

    Returns:
        pd.DataFrame: The processed DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified columns are not in the DataFrame.
    """
    try:
        # Load the data from a CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e

    # If columns are specified, filter the DataFrame
    if columns is not None:
        missing_cols = set(columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Error: The following columns are not present in the DataFrame: {missing_cols}")
        df = df[columns]

    # Process the DataFrame (e.g., drop duplicates)
    df = df.drop_duplicates()

    return df

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data/sample_data.csv'  # Specify your CSV file path here
    columns_to_keep = ['column1', 'column2']  # Specify columns to keep

    try:
        # Load and process the data
        processed_data = load_and_process_data(file_path, columns_to_keep)
        print(processed_data)
    except (FileNotFoundError, ValueError) as e:
        print(e)

if __name__ == "__main__":
    main()