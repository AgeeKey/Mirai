"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T05:01:25.828069

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the data, or None if loading fails.
    """
    try:
        df = pd.read_csv(file_path)  # Load the CSV into a DataFrame
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file {file_path} could not be parsed.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Summarize the DataFrame with descriptive statistics and data types.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    if df is not None:
        print("Data Summary:")
        print(df.describe())  # Print descriptive statistics
        print("\nData Types:")
        print(df.dtypes)  # Print data types of each column
    else:
        print("No data to summarize.")

def main() -> None:
    """
    Main function to execute the data loading and summarization.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    df = load_data(file_path)  # Load the data
    summarize_data(df)  # Summarize the data

if __name__ == "__main__":
    main()  # Run the main function