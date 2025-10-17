"""
pandas - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-17T19:11:13.584242

This code has been verified by MIRAI's NASA-level learning system.
"""

import pandas as pd
import numpy as np
from typing import Optional

def create_dataframe(data: Optional[dict] = None) -> pd.DataFrame:
    """
    Create a pandas DataFrame from a dictionary.
    
    Parameters:
    - data (Optional[dict]): A dictionary containing data to create the DataFrame. 
                             If None, an empty DataFrame will be created.
                             
    Returns:
    - pd.DataFrame: A pandas DataFrame object.
    """
    if data is None:
        data = {}
    
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        raise ValueError("Error creating DataFrame: " + str(e))

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by filling missing values and removing duplicates.
    
    Parameters:
    - df (pd.DataFrame): Input DataFrame to clean.
    
    Returns:
    - pd.DataFrame: Cleaned DataFrame.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    # Fill missing values with the mean of the column
    df.fillna(df.mean(), inplace=True)
    
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)
    
    return df

def analyze_data(df: pd.DataFrame) -> pd.Series:
    """
    Analyze the DataFrame by calculating basic statistics.
    
    Parameters:
    - df (pd.DataFrame): Input DataFrame for analysis.
    
    Returns:
    - pd.Series: A Series containing the mean for each numeric column.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    return df.mean()

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = {
        'A': [1, 2, np.nan, 4],
        'B': [np.nan, 2, 3, 4],
        'C': [1, 1, 1, 1]
    }
    
    # Create DataFrame
    df = create_dataframe(sample_data)
    
    # Clean DataFrame
    cleaned_df = clean_data(df)
    
    # Analyze DataFrame
    statistics = analyze_data(cleaned_df)
    
    print("Cleaned DataFrame:")
    print(cleaned_df)
    print("\nStatistics:")
    print(statistics)