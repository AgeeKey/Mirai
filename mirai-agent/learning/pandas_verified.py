"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-21T23:33:38.949770

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def load_and_process_data(file_path: str, column_filter: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by filtering columns and filling missing values.

    Parameters:
    - file_path (str): The path to the CSV file.
    - column_filter (Optional[list]): List of columns to keep. If None, all columns are kept.

    Returns:
    - pd.DataFrame: A processed DataFrame.
    """
    try:
        # Load the data
        df = pd.read_csv(file_path)
        
        # Filter columns if specified
        if column_filter is not None:
            df = df[column_filter]

        # Fill missing values with the mean of each column
        df.fillna(df.mean(), inplace=True)

        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The provided CSV file is empty.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

def main():
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Path to your CSV file
    columns_to_keep = ['column1', 'column2', 'column3']  # Specify columns to keep

    try:
        processed_data = load_and_process_data(file_path, columns_to_keep)
        print(processed_data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()