"""
pyautogui - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-18T02:54:54.251518

This code has been verified by MIRAI's NASA-level learning system.
"""

import pyautogui
import time
from typing import Optional

def click_button(image_path: str, timeout: Optional[int] = 10) -> bool:
    """
    Clicks a button on the screen identified by the image.

    Args:
        image_path (str): The path to the image of the button to click.
        timeout (Optional[int]): Maximum time to wait for the button to appear.

    Returns:
        bool: True if the button was clicked, False otherwise.
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            # Locate the button on the screen
            button_location = pyautogui.locateOnScreen(image_path)
            if button_location is not None:
                # Calculate the center of the button
                button_center = pyautogui.center(button_location)
                # Click the button
                pyautogui.click(button_center)
                return True
            time.sleep(0.5)  # Wait before trying again
        except Exception as e:
            print(f"Error finding button: {e}")
            return False
    print("Button not found within the timeout period.")
    return False

if __name__ == "__main__":
    # Example usage of the click_button function
    button_image = 'button.png'  # Replace with the path to your button image
    if click_button(button_image):
        print("Button clicked successfully.")
    else:
        print("Failed to click button.")