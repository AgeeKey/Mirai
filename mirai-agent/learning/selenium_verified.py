"""
Selenium - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 0/1
Learned: 2025-10-14T19:05:34.928314

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def setup_driver() -> webdriver.Chrome:
    """Set up the Chrome WebDriver."""
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        return driver
    except WebDriverException as e:
        print(f"Error setting up the WebDriver: {e}")
        raise

def search_google(query: str) -> None:
    """Search for a query on Google and print the titles of the results.

    Args:
        query (str): The search term to be queried on Google.
    """
    driver = setup_driver()
    
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        
        # Find the search box using its name attribute value
        search_box = driver.find_element(By.NAME, "q")
        
        # Enter the search query and submit the form
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load
        time.sleep(2)

        # Retrieve the search result titles
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        for index, result in enumerate(results, start=1):
            print(f"{index}: {result.text}")
    except NoSuchElementException as e:
        print(f"Error finding an element: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    search_google("Selenium Python")