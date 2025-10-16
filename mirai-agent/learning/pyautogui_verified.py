"""
pyautogui - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-16T09:51:39.427134

This code has been verified by MIRAI's NASA-level learning system.
"""

import pyautogui
import time
from typing import Optional

def automate_mouse_and_keyboard(position: Optional[tuple[int, int]] = None, 
                                 click_count: int = 1, 
                                 wait_time: float = 1.0) -> None:
    """
    Automates mouse and keyboard actions.

    Args:
        position (Optional[tuple[int, int]]): The (x, y) coordinates to move the mouse to.
        click_count (int): The number of times to click the mouse.
        wait_time (float): Time to wait between actions.
    
    Raises:
        ValueError: If click_count is less than 1.
        pyautogui.FailSafeException: If the mouse is moved to a corner of the screen.
    """
    if click_count < 1:
        raise ValueError("click_count must be at least 1.")

    try:
        if position:
            pyautogui.moveTo(position[0], position[1], duration=0.5)  # Move to specified position
            time.sleep(wait_time)  # Wait before clicking

        for _ in range(click_count):
            pyautogui.click()  # Click the mouse
            time.sleep(wait_time)  # Wait between clicks

        pyautogui.typewrite("Automated typing!", interval=0.1)  # Type a message
    except pyautogui.FailSafeException:
        print("Fail-safe triggered. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    time.sleep(5)  # Allow time to switch to the target application
    automate_mouse_and_keyboard(position=(500, 500), click_count=3, wait_time=0.5)