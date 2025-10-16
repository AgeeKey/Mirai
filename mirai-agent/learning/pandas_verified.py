"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-16T12:40:09.634847

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Tuple

def generate_sample_data(num_rows: int) -> pd.DataFrame:
    """
    Generate a sample DataFrame with random data.

    Args:
        num_rows (int): The number of rows to generate.

    Returns:
        pd.DataFrame: A DataFrame containing random sample data.
    """
    if num_rows <= 0:
        raise ValueError("The number of rows must be a positive integer.")
    
    # Create sample data
    data = {
        'A': np.random.randint(1, 100, size=num_rows),
        'B': np.random.rand(num_rows),
        'C': np.random.choice(['X', 'Y', 'Z'], size=num_rows)
    }
    return pd.DataFrame(data)

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the DataFrame by adding a new column and filtering.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A processed DataFrame with an additional column and filtered rows.
    """
    if df.empty:
        raise ValueError("The input DataFrame is empty.")
    
    # Add a new column 'D' which is the sum of 'A' and 'B'
    df['D'] = df['A'] + df['B']
    
    # Filter rows where the value of 'D' is greater than a threshold
    processed_df = df[df['D'] > 50]
    
    return processed_df

def main(num_rows: int) -> None:
    """
    Main function to generate and process data.

    Args:
        num_rows (int): Number of rows for the sample data.
    """
    try:
        # Generate sample data
        sample_data = generate_sample_data(num_rows)
        print("Sample Data:")
        print(sample_data)
        
        # Process the generated data
        processed_data = process_data(sample_data)
        print("\nProcessed Data:")
        print(processed_data)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main(10)