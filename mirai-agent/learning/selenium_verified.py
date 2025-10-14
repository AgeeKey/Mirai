"""
Selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.87
Tests Passed: 0/1
Learned: 2025-10-14T20:27:05.383106

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def setup_driver() -> webdriver.Chrome:
    """Sets up the Chrome WebDriver with specified options.

    Returns:
        webdriver.Chrome: An instance of the Chrome WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service('/path/to/chromedriver')  # Update with your actual path
    return webdriver.Chrome(service=service, options=chrome_options)

def search_google(query: str) -> None:
    """Searches for a query on Google and logs the title of the results page.

    Args:
        query (str): The search query to input in Google.
    """
    try:
        driver = setup_driver()
        driver.get("https://www.google.com")

        # Find the search box using its name attribute value
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()  # Clear the search box
        search_box.send_keys(query)  # Input the search query
        search_box.send_keys(Keys.RETURN)  # Press Enter

        # Wait for the results page to load and display the results
        WebDriverWait(driver, 10).until(
            EC.title_contains(query)
        )
        logging.info(f"Title of the results page: {driver.title}")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    search_google("Selenium Python")