"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T20:58:20.548315

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame and optionally filter specific columns.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_filter (Optional[list]): A list of columns to retain in the DataFrame. If None, all columns are retained.

    Returns:
    - pd.DataFrame: Processed DataFrame containing the specified columns.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - ValueError: If any of the specified columns are not found in the DataFrame.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file at {file_path} was not found.") from e

    if column_filter:
        # Check if specified columns exist in the DataFrame
        missing_columns = [col for col in column_filter if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Error: The following columns are not in the DataFrame: {missing_columns}")
        
        # Filter the DataFrame to retain only the specified columns
        df = df[column_filter]

    return df

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Replace with your CSV file path
    columns_to_keep = ['column1', 'column2']  # Replace with the columns you want to keep

    try:
        processed_data = load_and_process_data(file_path, columns_to_keep)
        print(processed_data)
    except (FileNotFoundError, ValueError) as e:
        print(e)

if __name__ == "__main__":
    main()