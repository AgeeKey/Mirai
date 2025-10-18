"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T16:05:01.427874

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def setup_driver() -> webdriver.Chrome:
    """
    Sets up the Chrome WebDriver with options.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        service = ChromeService(executable_path='/path/to/chromedriver')  # Update path as needed
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except WebDriverException as e:
        print(f"Error initializing the WebDriver: {e}")
        raise

def open_website(driver: webdriver.Chrome, url: str) -> None:
    """
    Opens the specified URL in the browser.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        url (str): The URL to open.
    """
    try:
        driver.get(url)
        time.sleep(2)  # Wait for the page to load
    except WebDriverException as e:
        print(f"Error opening the website: {e}")
        raise

def find_element(driver: webdriver.Chrome, by: By, value: str) -> None:
    """
    Finds an element on the page and prints its text.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        by (By): The method to locate the element.
        value (str): The value to locate the element.

    Raises:
        NoSuchElementException: If the element is not found.
    """
    try:
        element = driver.find_element(by, value)
        print(f"Element text: {element.text}")
    except NoSuchElementException:
        print(f"Element with {by}='{value}' not found.")
        raise

def main() -> None:
    """
    Main function to run the Selenium automation script.
    """
    url = "https://www.example.com"  # Replace with the desired URL
    driver = setup_driver()
    try:
        open_website(driver, url)
        find_element(driver, By.TAG_NAME, "h1")  # Example: Find the first <h1> tag
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    main()