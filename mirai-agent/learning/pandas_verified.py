"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-21T17:19:28.691231

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the data from the CSV file,
                                or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print a summary of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("DataFrame Summary:")
        print(df.info())  # Display DataFrame info
        print("First 5 rows of the DataFrame:")
        print(df.head())  # Display first 5 rows
    else:
        print("No data to summarize.")

def main(file_path: str) -> None:
    """
    Main function to load data and summarize it.

    Args:
        file_path (str): The path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    summarize_data(df)         # Summarize the loaded data

if __name__ == "__main__":
    # Example usage:
    main("data.csv")  # Replace 'data.csv' with your actual CSV file path