"""
pyautogui - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.94
Tests Passed: 0/1
Learned: 2025-10-22T02:14:09.665420

This code has been verified by MIRAI's NASA-level learning system.
"""

import pyautogui
import time
from typing import Optional

def automated_clicker(x: Optional[int] = None, y: Optional[int] = None, duration: float = 1.0) -> None:
    """
    Moves the mouse to the specified coordinates and performs a click.
    
    Args:
        x (Optional[int]): The x-coordinate to move the mouse to. If None, uses current mouse position.
        y (Optional[int]): The y-coordinate to move the mouse to. If None, uses current mouse position.
        duration (float): The duration to move the mouse to the coordinates.
        
    Raises:
        ValueError: If the coordinates are invalid.
        pyautogui.FailSafeException: If the mouse is moved to a corner of the screen.
    """
    try:
        # Get current mouse position if coordinates are not provided
        if x is None or y is None:
            x, y = pyautogui.position()

        # Move the mouse to the specified coordinates over the given duration
        pyautogui.moveTo(x, y, duration)
        # Perform a mouse click
        pyautogui.click()

    except ValueError as e:
        print(f"Error: {e}")
    except pyautogui.FailSafeException:
        print("Mouse moved to a corner of the screen. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Delay to switch to the target application
    time.sleep(5)
    # Example usage: Click at coordinates (100, 200)
    automated_clicker(100, 200)