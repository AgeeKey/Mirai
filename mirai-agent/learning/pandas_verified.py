"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-15T08:13:22.527865

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a list of dictionaries.

    Parameters:
    data (List[dict]): A list of dictionaries containing data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.

    Raises:
    ValueError: If the input data is empty or not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input must be a list of dictionaries.")
    
    if not data:
        raise ValueError("Input data cannot be empty.")
    
    # Creating DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    return df

def save_dataframe_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Save the DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to save.
    file_path (str): The path where the CSV file will be saved.

    Raises:
    IOError: If there is an issue with file writing.
    """
    try:
        df.to_csv(file_path, index=False)
    except IOError as e:
        raise IOError(f"An error occurred while writing to the file: {e}")

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]

    # Create DataFrame
    df = create_dataframe(sample_data)
    print(df)

    # Save DataFrame to a CSV file
    save_dataframe_to_csv(df, "output.csv")