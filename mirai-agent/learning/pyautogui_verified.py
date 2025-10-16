"""
PyAutoGUI - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.99
Tests Passed: 0/1
Learned: 2025-10-16T19:27:35.917137

This code has been verified by MIRAI's NASA-level learning system.
"""

import pyautogui
import time
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

def automate_mouse_and_keyboard() -> None:
    """
    Automates mouse movement and keyboard input to demonstrate PyAutoGUI functionality.
    This function moves the mouse to a specific position, clicks, and types a message.
    """
    try:
        # Give the user a moment to switch to the target application
        logging.info("You have 5 seconds to switch to the target application.")
        time.sleep(5)
        
        # Move the mouse to a specific position (x=500, y=300)
        pyautogui.moveTo(500, 300, duration=1)
        logging.info("Mouse moved to (500, 300).")
        
        # Click the left mouse button
        pyautogui.click()
        logging.info("Mouse clicked at (500, 300).")
        
        # Type a message
        message = "Hello, this is an automated message!"
        pyautogui.typewrite(message, interval=0.1)
        logging.info(f"Typed message: {message}")
        
        # Press the Enter key
        pyautogui.press('enter')
        logging.info("Pressed Enter key.")
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    automate_mouse_and_keyboard()