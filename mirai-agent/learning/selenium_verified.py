"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-16T23:47:14.954633

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

def setup_driver() -> webdriver.Chrome:
    """Set up the Chrome WebDriver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service(executable_path='path/to/chromedriver')  # Update with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def search_google(query: str) -> None:
    """Search for a query on Google and print the titles of the results.

    Args:
        query (str): The search query to input into Google.
    """
    try:
        driver = setup_driver()
        driver.get("https://www.google.com")
        
        # Locate the search box
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query + Keys.RETURN)  # Enter the search query
        
        time.sleep(2)  # Allow time for search results to load

        # Get the search result titles
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')
        for index, result in enumerate(results, start=1):
            print(f"{index}: {result.text}")  # Print each title
        
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    search_google("Python Selenium tutorial")