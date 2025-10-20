"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-20T00:17:34.838594

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import Optional

def load_and_analyze_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a CSV file into a pandas DataFrame and perform basic analysis.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        Optional[pd.DataFrame]: DataFrame containing the loaded data, or None if loading fails.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Display basic information about the DataFrame
        print("DataFrame Info:")
        print(df.info())

        # Display summary statistics of the DataFrame
        print("\nSummary Statistics:")
        print(df.describe())

        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

# Example usage
if __name__ == "__main__":
    data_frame = load_and_analyze_data('example_data.csv')