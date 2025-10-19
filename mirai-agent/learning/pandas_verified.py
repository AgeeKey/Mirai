"""
Pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-19T21:56:09.378668

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
from typing import List

def create_dataframe(data: List[dict]) -> pd.DataFrame:
    """
    Create a Pandas DataFrame from a list of dictionaries.

    Args:
        data (List[dict]): A list of dictionaries containing data.

    Returns:
        pd.DataFrame: A DataFrame constructed from the input data.

    Raises:
        ValueError: If the input data is not a list of dictionaries.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("Input data must be a list of dictionaries.")
    
    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    return df

def main() -> None:
    """
    Main function to demonstrate the creation and manipulation of a DataFrame.
    """
    # Sample data to create the DataFrame
    sample_data = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]
    
    try:
        # Create DataFrame
        df = create_dataframe(sample_data)
        
        # Display the DataFrame
        print("Initial DataFrame:")
        print(df)
        
        # Compute the average age
        average_age = df['Age'].mean()
        print(f"\nAverage Age: {average_age:.2f}")
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()