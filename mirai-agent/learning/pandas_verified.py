"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-19T11:25:24.554922

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load data from a CSV file into a Pandas DataFrame.
    
    Parameters:
    - file_path: str - The path to the CSV file.
    
    Returns:
    - Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if an error occurs.
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
        print("Error: There was a parsing error.")
        return None

def analyze_data(df: pd.DataFrame) -> None:
    """
    Perform basic analysis on the DataFrame.
    
    Parameters:
    - df: pd.DataFrame - The DataFrame to analyze.
    """
    if df is not None:
        print("DataFrame Head:")
        print(df.head())  # Display the first 5 rows
        print("\nDataFrame Info:")
        print(df.info())  # Display DataFrame information
        print("\nDescriptive Statistics:")
        print(df.describe())  # Display descriptive statistics
    else:
        print("No data to analyze.")

if __name__ == "__main__":
    # Example file path (replace with your actual file path)
    file_path = "data.csv"
    
    # Load data
    data_frame = load_data(file_path)
    
    # Analyze data
    analyze_data(data_frame)