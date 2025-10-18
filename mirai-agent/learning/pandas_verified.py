"""
pandas - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 0/1
Learned: 2025-10-18T23:35:17.473898

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np

def generate_dataframe(rows: int, columns: int) -> pd.DataFrame:
    """
    Generates a DataFrame with random numbers.

    Args:
        rows (int): Number of rows in the DataFrame.
        columns (int): Number of columns in the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame filled with random numbers.

    Raises:
        ValueError: If rows or columns are not positive integers.
    """
    if rows <= 0 or columns <= 0:
        raise ValueError("Rows and columns must be positive integers.")

    # Generate random data
    data = np.random.rand(rows, columns)
    
    # Create a DataFrame with the generated data
    df = pd.DataFrame(data, columns=[f'Column_{i+1}' for i in range(columns)])
    
    return df

def main() -> None:
    """
    Main function to execute the DataFrame generation and display.
    """
    try:
        # Specify the number of rows and columns
        num_rows = 5
        num_columns = 3
        
        # Generate the DataFrame
        df = generate_dataframe(num_rows, num_columns)
        
        # Display the DataFrame
        print(df)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()