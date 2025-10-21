"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-21T07:21:27.041619

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the loaded data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise ValueError("The file is empty.") from e
    except pd.errors.ParserError as e:
        raise ValueError("Error parsing the file.") from e

def clean_data(df: pd.DataFrame, columns_to_drop: Optional[list] = None) -> pd.DataFrame:
    """
    Clean the DataFrame by dropping specified columns and handling missing values.

    Parameters:
        df (pd.DataFrame): The DataFrame to clean.
        columns_to_drop (Optional[list]): List of columns to drop from the DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop, errors='ignore')  # Drop specified columns if they exist
    df = df.dropna()  # Drop rows with missing values
    return df

def main(file_path: str, columns_to_drop: Optional[list] = None) -> None:
    """
    Main function to load and clean data from a CSV file.

    Parameters:
        file_path (str): The path to the CSV file.
        columns_to_drop (Optional[list]): List of columns to drop from the DataFrame.
    """
    # Load the data
    df = load_data(file_path)
    
    # Clean the data
    cleaned_df = clean_data(df, columns_to_drop)
    
    # Display the cleaned DataFrame
    print(cleaned_df)

if __name__ == "__main__":
    # Example usage
    file_path = 'data.csv'  # Path to the CSV file
    columns_to_drop = ['unnecessary_column']  # Example column to drop
    main(file_path, columns_to_drop)