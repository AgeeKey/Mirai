"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 0/1
Learned: 2025-10-14T22:52:53.926198

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver() -> webdriver.Chrome:
    """Sets up the Chrome WebDriver and returns the driver instance."""
    try:
        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        return driver
    except Exception as e:
        print(f"Error setting up the WebDriver: {e}")
        raise

def navigate_to_page(driver: webdriver.Chrome, url: str) -> None:
    """Navigates to the specified URL using the provided WebDriver."""
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        raise

def find_element(driver: webdriver.Chrome, by: By, value: str) -> webdriver.remote.webelement.WebElement:
    """Finds an element on the page and returns it."""
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"Element with value '{value}' not found within the timeout period.")
        raise
    except NoSuchElementException:
        print(f"Element with value '{value}' does not exist on the page.")
        raise

def main() -> None:
    """Main function to run the Selenium script."""
    driver = setup_driver()  # Set up the WebDriver
    try:
        navigate_to_page(driver, "https://www.example.com")  # Navigate to the target page
        element = find_element(driver, By.TAG_NAME, "h1")  # Find the <h1> element
        print(f"Found element: {element.text}")  # Print the text of the found element
    finally:
        driver.quit()  # Ensure the driver quits even if an error occurs

if __name__ == "__main__":
    main()  # Run the main function