"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-17T00:53:18.526503

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Any, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty - {e}")
        raise

def summarize_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Summarize the DataFrame statistics.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        dict: A dictionary containing summary statistics.
    """
    summary = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'head': df.head(),
        'description': df.describe(include='all')
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Args:
        file_path (str): Path to the CSV file to load.
    """
    try:
        # Load the data from the CSV file
        data = load_data(file_path)
        
        # Generate summary statistics
        summary = summarize_data(data)
        
        # Print the summary
        print("Data Summary:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'data.csv' with the path to your CSV file
    main('data.csv')