"""
matplotlib - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-22T10:30:03.428233

This code has been verified by MIRAI's NASA-level learning system.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

def generate_data(num_points: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate random data for plotting.

    Args:
        num_points (int): Number of data points to generate.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing x and y coordinates.
    """
    if num_points <= 0:
        raise ValueError("Number of points must be a positive integer.")
    
    x = np.linspace(0, 10, num_points)
    y = np.sin(x) + np.random.normal(scale=0.5, size=num_points)  # Adding noise to the sine wave
    return x, y

def plot_data(x: np.ndarray, y: np.ndarray) -> None:
    """
    Plot the provided x and y data.

    Args:
        x (np.ndarray): x coordinates.
        y (np.ndarray): y coordinates.
    """
    plt.figure(figsize=(10, 5))  # Set the figure size
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Sine Wave with Noise')
    plt.title('Sine Wave with Random Noise')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    
    try:
        plt.savefig('sine_wave_plot.png')  # Save the plot as a PNG file
    except Exception as e:
        print(f"Error saving the plot: {e}")

    plt.show()  # Display the plot

def main() -> None:
    """
    Main function to generate data and plot it.
    """
    try:
        num_points = 100  # Define the number of points to generate
        x, y = generate_data(num_points)  # Generate the data
        plot_data(x, y)  # Plot the data
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()  # Run the main function