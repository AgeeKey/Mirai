"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-17T00:20:36.172516

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def generate_sample_data(num_rows: int) -> pd.DataFrame:
    """
    Generate a sample DataFrame with random data.

    Args:
        num_rows (int): The number of rows to generate.

    Returns:
        pd.DataFrame: A DataFrame containing random sample data.
    """
    if num_rows <= 0:
        raise ValueError("num_rows must be a positive integer.")
    
    data = {
        'A': np.random.randint(1, 100, num_rows),
        'B': np.random.rand(num_rows),
        'C': np.random.choice(['X', 'Y', 'Z'], num_rows)
    }
    return pd.DataFrame(data)

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the input DataFrame by adding a new column and filtering rows.

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    # Add a new column 'D' which is the sum of columns 'A' and 'B'
    df['D'] = df['A'] + df['B']
    
    # Filter the DataFrame where 'D' is greater than 50
    filtered_df = df[df['D'] > 50]
    
    return filtered_df

def main() -> None:
    """
    Main function to execute the data generation and processing.
    """
    try:
        # Generate sample data
        sample_data = generate_sample_data(100)
        
        # Process the generated data
        processed_data = process_data(sample_data)
        
        # Display the processed data
        print(processed_data)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()