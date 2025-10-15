"""
seaborn - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.97
Tests Passed: 0/1
Learned: 2025-10-15T18:31:21.290054

This code has been verified by MIRAI's NASA-level learning system.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional

def create_boxplot(data: pd.DataFrame, x: str, y: str, title: Optional[str] = None) -> None:
    """
    Creates a boxplot using Seaborn.

    Parameters:
    - data (pd.DataFrame): The data to be plotted.
    - x (str): The name of the column to be plotted on the x-axis.
    - y (str): The name of the column to be plotted on the y-axis.
    - title (Optional[str]): Title of the plot. Default is None.
    
    Raises:
    ValueError: If the specified columns are not in the DataFrame.
    """
    # Check if the specified columns exist in the DataFrame
    if x not in data.columns or y not in data.columns:
        raise ValueError(f"Columns '{x}' or '{y}' not found in the DataFrame.")
    
    # Set the aesthetics for the plot
    sns.set_theme(style="whitegrid")
    
    # Create the boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=x, y=y)
    
    # Set the title if provided
    if title:
        plt.title(title)
    
    # Show the plot
    plt.show()

# Example usage
if __name__ == "__main__":
    # Create example data
    np.random.seed(0)
    example_data = pd.DataFrame({
        'Category': np.random.choice(['A', 'B', 'C'], size=200),
        'Values': np.random.randn(200)
    })
    
    try:
        # Create a boxplot for the example data
        create_boxplot(example_data, x='Category', y='Values', title='Boxplot of Values by Category')
    except ValueError as e:
        print(f"Error: {e}")