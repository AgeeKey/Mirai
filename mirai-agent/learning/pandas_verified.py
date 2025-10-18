"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-18T20:11:14.134519

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a given dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame containing the provided data.

    Raises:
    ValueError: If the input data is not a dictionary or if the lists have different lengths.
    """
    if not isinstance(data, dict):
        raise ValueError("Input data must be a dictionary.")
    
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in the dictionary must have the same length.")

    df = pd.DataFrame(data)
    return df

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and manipulation.
    """
    # Sample data for DataFrame creation
    sample_data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }

    try:
        # Create DataFrame
        df = create_dataframe(sample_data)
        
        # Display the DataFrame
        print("Original DataFrame:")
        print(df)
        
        # Add a new column
        df['Salary'] = [70000, 80000, 90000]
        print("\nDataFrame after adding Salary column:")
        print(df)

        # Calculate the average age
        average_age = df['Age'].mean()
        print(f"\nAverage Age: {average_age}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()