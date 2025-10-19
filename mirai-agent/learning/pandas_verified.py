"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T20:05:49.349586

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file and perform basic processing.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the processed data, or None if loading fails.
    """
    try:
        # Load data from CSV file
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    # Display the first few rows of the dataframe
    print("Initial data loaded:")
    print(data.head())

    # Drop rows with any missing values
    data_cleaned = data.dropna()

    # Reset index after dropping rows
    data_cleaned.reset_index(drop=True, inplace=True)

    return data_cleaned

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'example_data.csv'  # Specify the path to your CSV file
    processed_data = load_and_process_data(file_path)

    if processed_data is not None:
        print("Processed data:")
        print(processed_data)

if __name__ == '__main__':
    main()