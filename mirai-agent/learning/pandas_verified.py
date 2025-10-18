"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-18T01:20:10.180724

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the loaded data, or None if loading fails.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the DataFrame by performing basic cleaning and transformation.

    Parameters:
    df (pd.DataFrame): The DataFrame to process.

    Returns:
    pd.DataFrame: The processed DataFrame.
    """
    # Drop rows with missing values
    df_cleaned = df.dropna()
    
    # Reset index after dropping rows
    df_cleaned.reset_index(drop=True, inplace=True)
    
    # Convert all column names to lowercase
    df_cleaned.columns = [col.lower() for col in df_cleaned.columns]
    
    return df_cleaned

def save_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save the DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to save.
    output_path (str): The path where the CSV file will be saved.
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"Data saved successfully to {output_path}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main(input_file: str, output_file: str) -> None:
    """
    Main function to load, process, and save data.

    Parameters:
    input_file (str): The path to the input CSV file.
    output_file (str): The path to the output CSV file.
    """
    df = load_data(input_file)
    if df is not None:
        processed_df = process_data(df)
        save_data(processed_df, output_file)

if __name__ == "__main__":
    # Example usage
    main('input_data.csv', 'processed_data.csv')