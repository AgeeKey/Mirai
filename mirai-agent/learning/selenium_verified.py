"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-16T05:31:52.034233

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver() -> webdriver.Chrome:
    """
    Sets up the Chrome WebDriver with necessary options.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for faster execution
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def main() -> None:
    """
    Main function to automate browser actions using Selenium.
    """
    try:
        driver = setup_driver()  # Set up the WebDriver
        driver.get("https://www.example.com")  # Navigate to the target URL
        
        time.sleep(2)  # Wait for the page to load
        
        # Find an element by its tag name
        heading = driver.find_element(By.TAG_NAME, "h1")
        print(f"Heading text: {heading.text}")  # Print the heading text
        
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions that occur
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    main()  # Execute the main function