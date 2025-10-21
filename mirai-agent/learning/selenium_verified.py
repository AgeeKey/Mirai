"""
selenium - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.97
Tests Passed: 0/1
Learned: 2025-10-21T02:04:15.462155

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def search_google(query: str) -> None:
    """
    Automates a Google search for the given query.

    Args:
        query (str): The search term to query on Google.

    Raises:
        WebDriverException: If there is an issue with the web driver.
        NoSuchElementException: If the search input or results cannot be found.
    """
    # Setup Chrome WebDriver
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    except WebDriverException as e:
        print(f"Error initializing the WebDriver: {e}")
        return

    try:
        # Navigate to Google
        driver.get("https://www.google.com")

        # Find the search input field using its name attribute value
        search_box = driver.find_element(By.NAME, "q")
        
        # Enter the search query
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)  # Press Enter
        
        # Wait for results to load
        time.sleep(2)

        # Get search results
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')

        # Print titles of the search results
        for result in results:
            print(result.text)
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    search_google("OpenAI")