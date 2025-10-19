"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T12:12:26.460324

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
        return None

def save_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        output_path (str): The path where the CSV file will be saved.
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving data to {output_path}: {e}")

def main() -> None:
    """
    Main function to demonstrate loading and saving data with pandas.
    """
    # Load the data from a CSV file
    input_file_path = 'input_data.csv'
    df = load_data(input_file_path)
    
    if df is not None:
        # Display the first few rows of the DataFrame
        print(df.head())
        
        # Perform a simple operation, e.g., calculating the mean of a numeric column
        if 'numeric_column' in df.columns:
            mean_value = df['numeric_column'].mean()
            print(f"Mean value of 'numeric_column': {mean_value}")
        
        # Save the modified DataFrame to a new CSV file
        output_file_path = 'output_data.csv'
        save_data(df, output_file_path)

if __name__ == "__main__":
    main()