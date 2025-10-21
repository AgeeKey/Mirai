"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-21T18:24:27.337137

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from pandas.errors import EmptyDataError

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load and process data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A processed DataFrame with cleaned data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        EmptyDataError: If the file is empty.
    """
    try:
        # Load the data from the CSV file
        data = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {file_path} was not found.") from e
    except EmptyDataError as e:
        raise EmptyDataError("The file is empty.") from e

    # Basic data cleaning: drop rows with any missing values
    cleaned_data = data.dropna()

    # Convert all column names to lowercase
    cleaned_data.columns = [col.lower() for col in cleaned_data.columns]

    return cleaned_data

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    try:
        processed_data = load_and_process_data(file_path)
        print(processed_data.head())  # Display the first few rows of the processed data
    except (FileNotFoundError, EmptyDataError) as e:
        print(e)

if __name__ == "__main__":
    main()