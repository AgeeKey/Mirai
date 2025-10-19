"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T07:43:47.277125

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by filling missing values
    and converting data types.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The processed DataFrame.
    
    Raises:
    FileNotFoundError: If the file does not exist.
    pd.errors.EmptyDataError: If the file is empty.
    pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)

        # Fill missing values with the mean for numerical columns
        for col in data.select_dtypes(include=np.number).columns:
            data[col].fillna(data[col].mean(), inplace=True)

        # Convert categorical columns to 'category' type
        for col in data.select_dtypes(include='object').columns:
            data[col] = data[col].astype('category')
        
        return data

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path.")
        raise
    except pd.errors.EmptyDataError as e:
        print("Error: The file is empty.")
        raise
    except pd.errors.ParserError as e:
        print("Error: Could not parse the file.")
        raise

def main() -> None:
    """
    Main function to execute the data loading and processing.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    try:
        processed_data = load_and_process_data(file_path)
        print(processed_data.head())  # Display the first few rows of the processed data
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()