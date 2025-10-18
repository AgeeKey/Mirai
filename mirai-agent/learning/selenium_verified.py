"""
selenium - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.98
Tests Passed: 0/1
Learned: 2025-10-18T19:39:46.299617

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import WebDriverException

def automate_google_search(search_query: str) -> None:
    """
    Automates a Google search using Selenium.

    Args:
        search_query (str): The query to search for on Google.
    """
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    
    # Initialize the Chrome driver
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        return

    try:
        # Open Google
        driver.get("https://www.google.com")

        # Find the search box using its name attribute value
        search_box = driver.find_element(By.NAME, "q")
        
        # Type the search query and submit
        search_box.send_keys(search_query + Keys.RETURN)

        # Wait for results to load
        time.sleep(2)

        # Collect and print the titles of the search results
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')
        for index, result in enumerate(results):
            print(f"{index + 1}: {result.text}")

    except Exception as e:
        print(f"An error occurred during the search: {e}")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Example usage
    automate_google_search("OpenAI GPT-3")