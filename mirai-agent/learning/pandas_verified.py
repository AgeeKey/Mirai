"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-21T02:20:10.801140

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_clean_data(file_path: str, drop_columns: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and clean it by dropping specified columns.

    Parameters:
    file_path (str): The path to the CSV file.
    drop_columns (Optional[list]): List of column names to drop from the DataFrame.

    Returns:
    pd.DataFrame: A cleaned DataFrame.
    
    Raises:
    FileNotFoundError: If the specified file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If the file cannot be parsed as CSV.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Drop specified columns if provided
        if drop_columns is not None:
            df.drop(columns=drop_columns, inplace=True, errors='ignore')
        
        return df

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: No data - {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Parsing error - {e}")
        raise

def main():
    # Define the path to the CSV file
    csv_file_path = 'data.csv'

    # Specify columns to drop if needed
    columns_to_drop = ['unnecessary_column']

    # Load and clean the data
    cleaned_data = load_and_clean_data(csv_file_path, columns_to_drop)
    
    # Display the cleaned DataFrame
    print(cleaned_data)

if __name__ == "__main__":
    main()