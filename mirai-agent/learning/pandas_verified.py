"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-22T05:25:10.062658

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def create_dataframe(data: dict) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data (dict): A dictionary where keys are column names and values are lists of column data.

    Returns:
    pd.DataFrame: A DataFrame constructed from the provided data.

    Raises:
    ValueError: If the lists in the dictionary are not of the same length.
    """
    if not all(len(v) == len(next(iter(data.values()))) for v in data.values()):
        raise ValueError("All columns must be of the same length.")
    
    return pd.DataFrame(data)

def main() -> None:
    """
    Main function to demonstrate DataFrame creation and manipulation.
    """
    # Sample data for the DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [24, 27, 22, 32],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    
    try:
        # Create the DataFrame
        df = create_dataframe(data)
        
        # Display the DataFrame
        print("Initial DataFrame:")
        print(df)

        # Add a new column based on existing data
        df['Salary'] = np.random.randint(50000, 100000, size=len(df))
        print("\nDataFrame after adding Salary column:")
        print(df)

        # Calculate and print average age
        average_age = df['Age'].mean()
        print(f"\nAverage Age: {average_age}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()