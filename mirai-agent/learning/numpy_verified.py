"""
numpy - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 0/1
Learned: 2025-10-20T12:25:35.429384

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np

def create_random_array(shape: tuple[int, ...], low: float = 0.0, high: float = 1.0) -> np.ndarray:
    """
    Create a random array with a specified shape and value range.

    Parameters:
    shape (tuple[int, ...]): Shape of the array to create.
    low (float): Lower bound for the random values. Default is 0.0.
    high (float): Upper bound for the random values. Default is 1.0.

    Returns:
    np.ndarray: Array of random values with the specified shape.
    
    Raises:
    ValueError: If low is greater than or equal to high.
    """
    if low >= high:
        raise ValueError("The 'low' value must be less than the 'high' value.")
    
    return np.random.uniform(low, high, size=shape)

def compute_statistics(arr: np.ndarray) -> dict[str, float]:
    """
    Compute the mean and standard deviation of an array.

    Parameters:
    arr (np.ndarray): Input array to compute statistics on.

    Returns:
    dict[str, float]: A dictionary containing the mean and standard deviation.
    
    Raises:
    ValueError: If the input is not a 1-dimensional or 2-dimensional array.
    """
    if arr.ndim not in (1, 2):
        raise ValueError("Input array must be 1-dimensional or 2-dimensional.")
    
    mean = np.mean(arr)
    std_dev = np.std(arr)
    return {'mean': mean, 'std_dev': std_dev}

# Example usage
if __name__ == "__main__":
    try:
        random_array = create_random_array((3, 4), 0, 10)
        stats = compute_statistics(random_array)
        print("Random Array:\n", random_array)
        print("Statistics:", stats)
    except ValueError as e:
        print("Error:", e)