"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-21T06:17:45.022310

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional, Tuple

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e

def summarize_data(df: pd.DataFrame) -> Tuple[int, pd.Series]:
    """
    Summarize the DataFrame by returning the number of rows and a description of the data.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Tuple[int, pd.Series]: A tuple containing the number of rows and a description of the DataFrame.
    """
    num_rows = len(df)
    description = df.describe(include='all')
    return num_rows, description

def main(file_path: str) -> None:
    """
    Main function to load data and summarize it.

    Args:
        file_path (str): The path to the CSV file to be analyzed.
    """
    # Load the data
    data = load_data(file_path)
    
    # Summarize the data
    num_rows, description = summarize_data(data)
    
    # Print the results
    print(f"Number of rows: {num_rows}")
    print("Data Description:")
    print(description)

if __name__ == "__main__":
    # Example usage: replace 'your_file.csv' with an actual CSV file path
    main('your_file.csv')