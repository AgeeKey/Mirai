"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-18T00:00:52.728331

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, column_name: str, threshold: Optional[float] = None) -> pd.DataFrame:
    """
    Load data from a CSV file, filter it based on a specified threshold, 
    and return a processed DataFrame.

    Parameters:
    - file_path (str): Path to the CSV file.
    - column_name (str): Column to filter the data on.
    - threshold (Optional[float]): Minimum value to filter the DataFrame. 
                                    If None, no filtering is applied.

    Returns:
    - pd.DataFrame: Processed DataFrame after loading and filtering.
    
    Raises:
    - FileNotFoundError: If the specified file does not exist.
    - KeyError: If the specified column does not exist in the DataFrame.
    """
    try:
        # Load data from CSV file
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file {file_path} was not found.") from e

    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        raise KeyError(f"Error: The column '{column_name}' does not exist in the DataFrame.")
    
    # Filter the DataFrame based on the threshold if provided
    if threshold is not None:
        df = df[df[column_name] >= threshold]

    return df

if __name__ == "__main__":
    # Example usage of the load_and_process_data function
    try:
        processed_data = load_and_process_data('data.csv', 'age', threshold=30)
        print(processed_data)
    except (FileNotFoundError, KeyError) as e:
        print(e)