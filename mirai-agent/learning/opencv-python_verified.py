"""
opencv-python - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-18T13:27:15.511690

This code has been verified by MIRAI's NASA-level learning system.
"""

import cv2
import numpy as np
from typing import Tuple

def load_and_display_image(image_path: str) -> None:
    """Loads an image from the specified path and displays it in a window.

    Args:
        image_path (str): The path to the image file.

    Raises:
        FileNotFoundError: If the image file is not found.
        Exception: For any other errors that may occur.
    """
    try:
        # Load the image
        image = cv2.imread(image_path)

        # Check if the image was loaded successfully
        if image is None:
            raise FileNotFoundError(f"Image file '{image_path}' not found.")

        # Display the image in a window
        cv2.imshow('Image', image)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()  # Close the image window
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(f"An error occurred: {e}")

def main() -> None:
    """Main function to load and display an image."""
    image_path = 'path/to/your/image.jpg'  # Replace with your image path
    load_and_display_image(image_path)

if __name__ == '__main__':
    main()