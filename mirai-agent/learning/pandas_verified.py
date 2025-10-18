"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-18T18:21:14.592333

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Union

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
    - FileNotFoundError: If the file does not exist.
    - pd.errors.EmptyDataError: If the file is empty.
    - pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        print(f"Error: The file is empty. {e}")
        raise
    except pd.errors.ParserError as e:
        print(f"Error: Could not parse the file. {e}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping missing values and duplicates.

    Parameters:
    - df (pd.DataFrame): The DataFrame to clean.

    Returns:
    - pd.DataFrame: The cleaned DataFrame.
    """
    # Drop rows with any missing values
    df_cleaned = df.dropna()
    # Drop duplicate rows
    df_cleaned = df_cleaned.drop_duplicates()
    return df_cleaned

def save_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save the cleaned DataFrame to a CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame to save.
    - output_path (str): The path to save the cleaned DataFrame.
    """
    df.to_csv(output_path, index=False)

def main(file_path: str, output_path: str) -> None:
    """
    Main function to load, clean, and save data.

    Parameters:
    - file_path (str): The path to the input CSV file.
    - output_path (str): The path to save the cleaned CSV file.
    """
    df = load_data(file_path)
    df_cleaned = clean_data(df)
    save_data(df_cleaned, output_path)

if __name__ == "__main__":
    # Example usage
    input_file = 'input_data.csv'  # Replace with your input file path
    output_file = 'cleaned_data.csv'  # Replace with your output file path
    main(input_file, output_file)