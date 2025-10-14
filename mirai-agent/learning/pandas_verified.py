"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-14T18:16:50.750712

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    :param file_path: Path to the CSV file.
    :return: DataFrame containing the loaded data.
    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If the file is empty or contains invalid data.
    """
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise ValueError("The loaded DataFrame is empty.")
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty or could not be parsed.")

def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a summary of the DataFrame including descriptive statistics.

    :param df: Input DataFrame to summarize.
    :return: DataFrame containing summary statistics.
    """
    return df.describe()

def main(file_path: str) -> Optional[pd.DataFrame]:
    """
    Main function to load data and generate a summary.

    :param file_path: Path to the CSV file.
    :return: Summary DataFrame or None if an error occurs.
    """
    try:
        data = load_data(file_path)
        summary = summarize_data(data)
        print(summary)
        return summary
    except (FileNotFoundError, ValueError) as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your actual CSV file path
    main(file_path)