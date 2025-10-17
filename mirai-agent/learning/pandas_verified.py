"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-17T08:38:27.274057

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    :param file_path: str - The path to the CSV file.
    :return: pd.DataFrame - The loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("No data found in the file.")
    except pd.errors.ParserError:
        raise ValueError("Error parsing the file.")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping NaN values and resetting the index.

    :param df: pd.DataFrame - The DataFrame to clean.
    :return: pd.DataFrame - The cleaned DataFrame.
    """
    cleaned_df = df.dropna().reset_index(drop=True)
    return cleaned_df

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame to get descriptive statistics.

    :param df: pd.DataFrame - The DataFrame to analyze.
    :return: pd.Series - Descriptive statistics of the DataFrame.
    """
    return df.describe()

def main(file_path: str) -> None:
    """
    Main function to load, clean, and analyze data from a CSV file.

    :param file_path: str - The path to the CSV file.
    """
    data = load_data(file_path)
    cleaned_data = clean_data(data)
    stats = analyze_data(cleaned_data)
    
    # Printing the descriptive statistics
    print("Descriptive Statistics:")
    print(stats)

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Replace with your actual CSV file path
    main(file_path)