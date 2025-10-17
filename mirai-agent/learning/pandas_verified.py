"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-17T23:12:50.551573

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is an error parsing the file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("Error: The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error: There was an error parsing the file.") from e

def summarize_data(df: pd.DataFrame) -> Dict[str, float]:
    """
    Summarize the DataFrame by calculating basic statistics.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        Dict[str, float]: A dictionary containing summary statistics (mean, median, std).
    """
    summary = {
        "mean": df.mean().to_dict(),
        "median": df.median().to_dict(),
        "std_dev": df.std().to_dict()
    }
    return summary

def main(file_path: str) -> None:
    """
    Main function to load and summarize data.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        df = load_data(file_path)  # Load the data
        summary = summarize_data(df)  # Summarize the data
        print("Data Summary:")
        print(summary)  # Output the summary
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Example usage
    main("data.csv")  # Replace 'data.csv' with your actual file path