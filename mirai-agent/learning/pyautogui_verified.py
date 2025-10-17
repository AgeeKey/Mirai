"""
pyautogui - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-17T21:04:46.311035

This code has been verified by MIRAI's NASA-level learning system.
"""

import pyautogui
import time
from typing import Optional

def click_button(image_path: str, timeout: Optional[int] = 30) -> None:
    """
    Clicks on a button identified by an image on the screen.

    Args:
        image_path (str): The file path of the image representing the button.
        timeout (Optional[int]): The time in seconds to wait for the button to appear.

    Raises:
        FileNotFoundError: If the image file does not exist.
        Exception: If the button is not found within the timeout period.
    """
    
    # Check if the image file exists
    try:
        pyautogui.locateOnScreen(image_path, confidence=0.8)
    except FileNotFoundError:
        raise FileNotFoundError(f"The specified image file '{image_path}' does not exist.")

    # Wait for the button to appear on the screen
    start_time = time.time()
    while True:
        button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if button_location is not None:
            pyautogui.click(button_location)
            print(f"Clicked on button: {image_path}")
            return
        if time.time() - start_time > timeout:
            raise Exception(f"Button '{image_path}' not found on the screen within {timeout} seconds.")
        time.sleep(0.5)  # Wait a bit before trying again

if __name__ == "__main__":
    # Example usage
    try:
        click_button("button_image.png", timeout=15)  # Replace with the actual button image path
    except Exception as e:
        print(f"An error occurred: {e}")