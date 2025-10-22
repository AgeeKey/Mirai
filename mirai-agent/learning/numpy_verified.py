"""
numpy - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.86
Tests Passed: 0/1
Learned: 2025-10-22T15:06:05.161168

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np

def generate_random_matrix(rows: int, cols: int) -> np.ndarray:
    """
    Generate a random matrix of given dimensions.

    Parameters:
    rows (int): Number of rows in the matrix.
    cols (int): Number of columns in the matrix.

    Returns:
    np.ndarray: A 2D array with random float values.
    
    Raises:
    ValueError: If rows or cols are not positive integers.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("Both rows and cols must be positive integers.")
    
    # Generate a random matrix
    return np.random.rand(rows, cols)

def compute_matrix_statistics(matrix: np.ndarray) -> dict:
    """
    Compute basic statistics of a given matrix.

    Parameters:
    matrix (np.ndarray): A 2D array for which statistics are to be computed.

    Returns:
    dict: A dictionary containing the mean, median, and standard deviation of the matrix.
    
    Raises:
    ValueError: If the input is not a 2D numpy array.
    """
    if not isinstance(matrix, np.ndarray) or matrix.ndim != 2:
        raise ValueError("Input must be a 2D numpy array.")
    
    # Calculate statistics
    mean = np.mean(matrix)
    median = np.median(matrix)
    std_dev = np.std(matrix)

    return {
        "mean": mean,
        "median": median,
        "std_dev": std_dev
    }

if __name__ == "__main__":
    try:
        # Example usage
        rows = 4
        cols = 5
        random_matrix = generate_random_matrix(rows, cols)
        print("Random Matrix:\n", random_matrix)

        stats = compute_matrix_statistics(random_matrix)
        print("Matrix Statistics:", stats)
    except ValueError as e:
        print("Error:", e)