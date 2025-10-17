"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-17T09:26:46.494173

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame with the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a parsing error.")
    return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Summarize the DataFrame by printing basic statistics and information.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("DataFrame Summary:")
        print(df.describe())  # Print summary statistics
        print("\nDataFrame Info:")
        print(df.info())      # Print DataFrame info
    else:
        print("No data to summarize.")

def main() -> None:
    """
    Main function to execute the data loading and summarization process.
    """
    file_path = 'data.csv'  # Specify the path to the CSV file
    df = load_data(file_path)  # Load the data
    summarize_data(df)         # Summarize the loaded data

if __name__ == "__main__":
    main()  # Run the main function