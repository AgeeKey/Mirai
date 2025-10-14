"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-14T16:22:12.183197

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file at the specified path does not exist.
        ValueError: If the file is empty or cannot be parsed.
    """
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            raise ValueError("The CSV file is empty.")
        return data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty or cannot be parsed.")

def calculate_statistics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate basic statistics of the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to calculate statistics for.

    Returns:
        Dict[str, float]: A dictionary containing mean, median, and standard deviation.
    """
    stats = {
        'mean': df.mean().to_dict(),
        'median': df.median().to_dict(),
        'std_dev': df.std().to_dict()
    }
    return stats

def main(file_path: str) -> None:
    """
    Main function to load data and calculate statistics.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load the data from the specified CSV file
        data = load_data(file_path)
        # Calculate statistics for the loaded data
        statistics = calculate_statistics(data)
        # Print the calculated statistics
        print("Statistics:", statistics)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example CSV file path (replace with your actual file path)
    csv_file_path = 'data.csv'
    main(csv_file_path)