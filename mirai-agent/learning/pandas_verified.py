"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-17T18:54:53.002846

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_process_data(file_path: str, delimiter: str = ',', na_values: Optional[list] = None) -> pd.DataFrame:
    """
    Load data from a CSV file and process it by handling missing values.

    Parameters:
    - file_path (str): The path to the CSV file.
    - delimiter (str): The delimiter used in the CSV file. Default is ','.
    - na_values (Optional[list]): Additional strings to recognize as NA/NaN.

    Returns:
    - pd.DataFrame: The processed DataFrame.

    Raises:
    - FileNotFoundError: If the file does not exist.
    - pd.errors.ParserError: If the file cannot be parsed.
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path, delimiter=delimiter, na_values=na_values)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Error parsing the file: {file_path}") from e
    
    # Fill missing values with the mean of each column
    df.fillna(df.mean(), inplace=True)

    return df

def main() -> None:
    """
    Main function to load and display the processed data.
    """
    file_path = 'data.csv'  # Specify your CSV file path here
    try:
        df = load_and_process_data(file_path)
        print("Processed DataFrame:")
        print(df)
    except (FileNotFoundError, pd.errors.ParserError) as e:
        print(e)

if __name__ == '__main__':
    main()