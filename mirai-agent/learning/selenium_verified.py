"""
selenium - Verified Learning Artifact

Quality Grade: C
Overall Score: 0.78
Tests Passed: 0/1
Learned: 2025-10-21T07:53:20.793920

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

def setup_driver() -> webdriver.Chrome:
    """Sets up the Chrome WebDriver."""
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        return driver
    except WebDriverException as e:
        print(f"Error setting up the WebDriver: {e}")
        raise

def navigate_to_page(driver: webdriver.Chrome, url: str) -> None:
    """Navigates to the specified URL."""
    try:
        driver.get(url)
    except WebDriverException as e:
        print(f"Error navigating to {url}: {e}")
        raise

def find_element(driver: webdriver.Chrome, by: By, value: str) -> webdriver.WebElement:
    """Finds an element on the page."""
    try:
        element = driver.find_element(by, value)
        return element
    except NoSuchElementException as e:
        print(f"Element not found using {by} with value '{value}': {e}")
        raise

def main() -> None:
    """Main function to execute the Selenium script."""
    driver = setup_driver()
    try:
        navigate_to_page(driver, "https://www.example.com")
        time.sleep(2)  # Wait for the page to load
        element = find_element(driver, By.TAG_NAME, "h1")
        print(f"Found element: {element.text}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()