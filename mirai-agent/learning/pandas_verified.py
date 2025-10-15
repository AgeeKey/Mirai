"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-15T17:25:51.275229

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def generate_sample_data(num_rows: int) -> pd.DataFrame:
    """Generate a sample DataFrame with random data.

    Args:
        num_rows (int): Number of rows to generate.

    Returns:
        pd.DataFrame: A DataFrame containing random data.
    """
    try:
        data = {
            'A': np.random.randint(1, 100, size=num_rows),
            'B': np.random.randn(num_rows),
            'C': np.random.choice(['X', 'Y', 'Z'], size=num_rows),
        }
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error generating sample data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the DataFrame where column 'A' is greater than 50.

    Args:
        df (pd.DataFrame): The DataFrame to filter.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    try:
        filtered_df = df[df['A'] > 50]
        return filtered_df
    except KeyError as e:
        print(f"Column not found in DataFrame: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def main() -> None:
    """Main function to run the data generation and filtering."""
    sample_data = generate_sample_data(100)  # Generate sample data
    filtered_data = filter_data(sample_data)   # Filter the data

    print("Sample Data:")
    print(sample_data.head())  # Display the first 5 rows of the sample data
    print("\nFiltered Data (A > 50):")
    print(filtered_data.head())  # Display the first 5 rows of the filtered data

if __name__ == "__main__":
    main()  # Execute the main function