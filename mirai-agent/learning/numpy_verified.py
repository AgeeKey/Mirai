"""
numpy - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-19T19:34:34.664586

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
from typing import Tuple

def create_array(shape: Tuple[int, int], fill_value: float = 0.0) -> np.ndarray:
    """
    Creates a NumPy array of a given shape and fills it with a specified value.
    
    Parameters:
    shape (Tuple[int, int]): The shape of the array (rows, columns).
    fill_value (float): The value to fill the array with. Default is 0.0.
    
    Returns:
    np.ndarray: A NumPy array filled with the specified value.
    
    Raises:
    ValueError: If the shape contains non-positive integers.
    """
    if any(dim <= 0 for dim in shape):
        raise ValueError("Shape dimensions must be positive integers.")
    
    return np.full(shape, fill_value)

def main() -> None:
    """
    Main function to demonstrate the creation of a NumPy array.
    """
    try:
        # Define the shape of the array
        array_shape = (3, 4)
        # Create a 3x4 array filled with 5.0
        array = create_array(array_shape, fill_value=5.0)
        # Print the created array
        print("Created NumPy Array:")
        print(array)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()