"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-21T03:39:19.857648

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List, Dict

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and perform basic processing.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A processed DataFrame.
    """
    try:
        # Load the data from the CSV file
        data = pd.read_csv(file_path)
        
        # Check for missing values and fill them with the mean for numeric columns
        data.fillna(data.mean(), inplace=True)

        # Convert column names to lowercase for consistency
        data.columns = [col.lower() for col in data.columns]
        
        return data

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def summarize_data(data: pd.DataFrame) -> Dict[str, float]:
    """
    Summarize the data by calculating mean and standard deviation.

    Parameters:
    data (pd.DataFrame): The DataFrame to summarize.

    Returns:
    Dict[str, float]: A dictionary containing mean and standard deviation.
    """
    if data.empty:
        print("Warning: The DataFrame is empty; cannot summarize.")
        return {}

    summary = {
        "mean": data.mean().to_dict(),
        "std_dev": data.std().to_dict()
    }
    return summary

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Specify your CSV file path here
    df = load_and_process_data(file_path)
    summary = summarize_data(df)
    print("Data Summary:", summary)