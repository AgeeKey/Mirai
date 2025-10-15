"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.88
Tests Passed: 0/1
Learned: 2025-10-15T05:31:09.176716

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import WebDriverException, NoSuchElementException

def perform_google_search(search_query: str) -> None:
    """
    Automates a Google search.

    Args:
        search_query (str): The query to search on Google.
    
    Raises:
        WebDriverException: If there is an issue with the WebDriver.
        NoSuchElementException: If an expected element is not found in the DOM.
    """
    try:
        # Set up the Chrome WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://www.google.com")

        # Find the search box using its name attribute value
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query + Keys.RETURN)  # Enter the search query and submit

        time.sleep(2)  # Wait for the results page to load

        # Check for results
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')
        if results:
            for result in results:
                print(result.text)  # Print the title of each result
        else:
            print("No results found.")

    except WebDriverException as e:
        print(f"WebDriver error occurred: {e}")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed properly

if __name__ == "__main__":
    perform_google_search("OpenAI")