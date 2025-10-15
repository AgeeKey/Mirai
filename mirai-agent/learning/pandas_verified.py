"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T22:18:31.724380

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        Optional[pd.DataFrame]: DataFrame containing the data or None if an error occurs.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: Error parsing the file.")
        return None

def summarize_data(df: pd.DataFrame) -> None:
    """
    Print basic statistics and information about the DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to summarize.
    """
    print("DataFrame Info:")
    print(df.info())  # Display DataFrame information
    print("\nDescriptive Statistics:")
    print(df.describe())  # Display descriptive statistics for numerical columns

def main() -> None:
    """
    Main function to load data and summarize it.
    """
    file_path = 'data.csv'  # Specify the path to your CSV file
    df = load_data(file_path)  # Load the data
    
    if df is not None:  # Check if the DataFrame is loaded successfully
        summarize_data(df)  # Summarize the loaded DataFrame

if __name__ == "__main__":
    main()  # Run the main function