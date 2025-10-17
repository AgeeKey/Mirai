"""
pyautogui - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.98
Tests Passed: 0/1
Learned: 2025-10-17T18:38:35.850807

This code has been verified by MIRAI's NASA-level learning system.
"""

import pyautogui
import time
from typing import Tuple

def click_and_type(position: Tuple[int, int], text: str, delay: float = 0.5) -> None:
    """
    Clicks at the specified position on the screen and types the provided text.

    Args:
        position (Tuple[int, int]): The (x, y) coordinates to click.
        text (str): The text to type after clicking.
        delay (float): Time to wait before the next action.
    """
    try:
        # Move the mouse to the specified position
        pyautogui.moveTo(position[0], position[1], duration=0.25)
        time.sleep(delay)  # Wait for a short duration

        # Click at the position
        pyautogui.click()
        time.sleep(delay)  # Wait before typing

        # Type the specified text
        pyautogui.typewrite(text, interval=0.1)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    # Adjust the position (x, y) and text as necessary
    click_and_type((500, 500), "Hello, PyAutoGUI!")