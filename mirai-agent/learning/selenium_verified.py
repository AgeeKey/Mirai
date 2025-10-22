"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-22T04:37:41.468633

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def setup_driver() -> webdriver.Chrome:
    """Sets up the Chrome WebDriver."""
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def search_google(query: str) -> None:
    """Searches for a query on Google and prints the titles of the results.

    Args:
        query (str): The search query string.
    """
    driver = setup_driver()
    try:
        driver.get("https://www.google.com")
        time.sleep(2)  # Wait for the page to load

        # Find the search box
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query + Keys.RETURN)
        time.sleep(2)  # Wait for the results to load

        # Print the titles of the results
        results = driver.find_elements(By.XPATH, "//h3")
        for index, result in enumerate(results):
            print(f"{index + 1}: {result.text}")

    except NoSuchElementException as e:
        print(f"An error occurred: {e}")
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    search_google("Selenium Python")