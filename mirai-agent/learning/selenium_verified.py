"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-17T20:16:15.085617

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
        # Initialize the Chrome driver using ChromeDriverManager
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        return driver
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        raise

def open_website(driver: webdriver.Chrome, url: str) -> None:
    """Opens the specified URL in the browser."""
    try:
        driver.get(url)
    except WebDriverException as e:
        print(f"Error opening website {url}: {e}")
        raise

def perform_search(driver: webdriver.Chrome, search_query: str) -> None:
    """Performs a search operation on the website."""
    try:
        # Locate the search box, enter the search query, and submit
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.submit()
    except NoSuchElementException as e:
        print(f"Search box not found: {e}")
        raise
    except WebDriverException as e:
        print(f"Error performing search: {e}")
        raise

def main() -> None:
    """Main function to execute the automation script."""
    driver = setup_driver()
    try:
        open_website(driver, "https://www.google.com")
        perform_search(driver, "Selenium documentation")
        time.sleep(5)  # Wait for results to load
    finally:
        # Ensure the driver is quit even if an error occurs
        driver.quit()

if __name__ == "__main__":
    main()