"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-18T07:39:42.200781

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file into a Pandas DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If there is a parsing error.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError("The file is empty.") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError("Error parsing the file.") from e

def clean_data(df: pd.DataFrame, columns_to_drop: Optional[list] = None) -> pd.DataFrame:
    """Clean the DataFrame by dropping specified columns and handling missing values.
    
    Args:
        df (pd.DataFrame): The DataFrame to clean.
        columns_to_drop (Optional[list]): List of columns to drop from the DataFrame.
        
    Returns:
        pd.DataFrame: A cleaned DataFrame.
    """
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop, errors='ignore')  # Drop columns if they exist
    
    df = df.dropna()  # Drop rows with missing values
    return df

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """Analyze the DataFrame and return summary statistics.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        
    Returns:
        pd.Series: Summary statistics of the DataFrame.
    """
    return df.describe()  # Get summary statistics

if __name__ == "__main__":
    # Example usage
    try:
        # Load the data
        data_frame = load_data('data.csv')
        
        # Clean the data
        cleaned_data = clean_data(data_frame, columns_to_drop=['unnecessary_column'])
        
        # Analyze the data
        summary_statistics = analyze_data(cleaned_data)
        
        # Print the summary statistics
        print(summary_statistics)
        
    except Exception as e:
        print(f"An error occurred: {e}")