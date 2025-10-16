"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-16T12:53:26.874469

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict, Any

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise

def summarize_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Summarize the given DataFrame by providing basic statistics.

    Args:
        df (pd.DataFrame): DataFrame to summarize.

    Returns:
        Dict[str, Any]: Dictionary containing summary statistics.
    """
    summary = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'head': df.head().to_dict(orient='records'),
        'describe': df.describe(include='all').to_dict()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load data and summarize it.

    Args:
        file_path (str): Path to the CSV file.
    """
    df = load_data(file_path)  # Load the data
    summary = summarize_data(df)  # Summarize the data
    print("Data Summary:")
    print(summary)

if __name__ == "__main__":
    # Example file path (update this to a valid CSV file path)
    example_file_path = 'data/example.csv'
    main(example_file_path)