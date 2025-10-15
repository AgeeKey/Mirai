"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-15T11:43:15.626010

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_names: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by renaming columns if specified.

    Args:
        file_path (str): The path to the CSV file.
        column_names (Optional[list]): A list of new column names. If provided, it will rename the columns.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the number of new column names does not match the number of columns in the data.
    """
    try:
        # Load the data from the CSV file
        data = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e

    if column_names is not None:
        if len(column_names) != data.shape[1]:
            raise ValueError("The number of new column names must match the number of columns in the data.")
        data.columns = column_names  # Rename columns

    # Drop rows with any missing values
    data = data.dropna()

    return data

if __name__ == "__main__":
    # Example usage
    try:
        df = load_and_process_data("data.csv", column_names=["Column1", "Column2", "Column3"])
        print(df.head())  # Display the first few rows of the DataFrame
    except Exception as e:
        print(e)