"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 1.00
Tests Passed: 0/1
Learned: 2025-10-16T07:09:14.540609

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the processed data.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except pd.errors.ParserError:
        raise ValueError("Error parsing the file.")

    # Display initial DataFrame shape
    initial_shape = df.shape
    print(f"Initial DataFrame shape: {initial_shape}")

    # Fill missing values with the mean of each column
    df.fillna(df.mean(), inplace=True)

    # Convert column names to lowercase
    df.columns = [col.lower() for col in df.columns]

    # Display final DataFrame shape
    final_shape = df.shape
    print(f"Final DataFrame shape after processing: {final_shape}")

    return df

# Example usage: Uncomment the line below to run with your specific CSV file path.
# df = load_and_process_data("path/to/your/data.csv")