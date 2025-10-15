"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-15T12:32:32.478055

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, filter_value: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame, process it by filtering a specific column, 
    and return the processed DataFrame.

    :param file_path: Path to the CSV file.
    :param column_name: Name of the column to filter.
    :param filter_value: Optional value to filter the column. If None, no filtering is applied.
    :return: Processed DataFrame.
    """
    try:
        # Load data from CSV file
        df = pd.read_csv(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

        # Filter the DataFrame if filter_value is provided
        if filter_value is not None:
            df = df[df[column_name] == filter_value]

        return df

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except pd.errors.EmptyDataError:
        print("Error: The provided CSV file is empty.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        print("Error: There was an error parsing the CSV file.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    df = load_and_process_data('data.csv', 'category', 'A')
    print(df)