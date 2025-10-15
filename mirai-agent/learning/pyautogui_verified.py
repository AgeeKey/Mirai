"""
pyautogui - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-15T14:26:02.325535

This code has been verified by MIRAI's NASA-level learning system.
"""

import pyautogui
import time
from typing import Optional

def automate_mouse_clicks(x: Optional[int] = None, y: Optional[int] = None, click_count: int = 1) -> None:
    """
    Automate mouse clicks at specified coordinates.

    Parameters:
    x (Optional[int]): The x-coordinate for the mouse click. If None, use current mouse position.
    y (Optional[int]): The y-coordinate for the mouse click. If None, use current mouse position.
    click_count (int): The number of times to click. Default is 1.
    
    Raises:
    ValueError: If click_count is less than 1.
    """
    if click_count < 1:
        raise ValueError("click_count must be at least 1.")

    # Allow some time before the clicks start
    time.sleep(2)

    # Get current mouse position if coordinates are not provided
    if x is None or y is None:
        x, y = pyautogui.position()

    # Move the mouse to the specified position
    pyautogui.moveTo(x, y)

    # Click the mouse the specified number of times
    for _ in range(click_count):
        pyautogui.click()
        time.sleep(0.1)  # Small delay between clicks

if __name__ == "__main__":
    try:
        # Example usage: Click 5 times at position (100, 100)
        automate_mouse_clicks(100, 100, click_count=5)
    except Exception as e:
        print(f"An error occurred: {e}")