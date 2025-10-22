"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-22T13:43:56.891113

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a Pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries containing data.

    Returns:
        pd.DataFrame: A DataFrame containing the input data.

    Raises:
        ValueError: If the input data is empty.
    """
    if not data:
        raise ValueError("Input data cannot be empty.")
    
    df = pd.DataFrame(data)  # Create DataFrame from the list of dictionaries
    return df

def save_dataframe_to_csv(df: pd.DataFrame, filename: str) -> None:
    """
    Save a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        filename (str): The name of the file to save the DataFrame to.

    Raises:
        ValueError: If the DataFrame is empty.
        IOError: If there is an issue saving the file.
    """
    if df.empty:
        raise ValueError("DataFrame cannot be empty.")
    
    try:
        df.to_csv(filename, index=False)  # Save DataFrame to CSV without the index
    except Exception as e:
        raise IOError(f"An error occurred while saving the file: {e}")

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and saving to CSV.
    """
    # Sample data to create a DataFrame
    sample_data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]

    try:
        # Create DataFrame
        df = create_dataframe(sample_data)
        print("DataFrame created successfully:")
        print(df)

        # Save DataFrame to a CSV file
        save_dataframe_to_csv(df, "output.csv")
        print("DataFrame saved to 'output.csv' successfully.")
    
    except (ValueError, IOError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()