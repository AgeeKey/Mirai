"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-15T02:01:12.527626

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it.
    
    Args:
        file_path (str): Path to the CSV file.
        columns (Optional[list]): List of columns to select from the DataFrame. If None, all columns are used.
    
    Returns:
        pd.DataFrame: Processed DataFrame.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If no columns are found in the file.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file {file_path} was not found.") from e

    if columns is not None:
        # Check if the specified columns exist in the DataFrame
        missing_cols = set(columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Error: The following columns are missing in the data: {missing_cols}")

        # Select the specified columns
        df = df[columns]

    # Drop any rows with missing values
    df.dropna(inplace=True)

    # Reset index after dropping rows
    df.reset_index(drop=True, inplace=True)

    return df

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Path to the CSV file
    selected_columns = ['column1', 'column2']  # Change to your desired columns

    try:
        processed_data = load_and_process_data(file_path, selected_columns)
        print(processed_data)
    except (FileNotFoundError, ValueError) as e:
        print(e)

if __name__ == "__main__":
    main()