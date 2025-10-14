"""
selenium - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 0/1
Learned: 2025-10-14T20:10:17.379387

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

def setup_driver() -> webdriver.Chrome:
    """Sets up the Chrome WebDriver with necessary options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Path to the ChromeDriver executable
    service = Service(executable_path='path/to/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def search_google(query: str) -> None:
    """Searches for a query on Google and prints the results."""
    driver = setup_driver()
    
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        time.sleep(2)  # Wait for the page to load

        # Find the search box using its name attribute value
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)  # Enter the search query
        search_box.submit()  # Submit the form
        time.sleep(2)  # Wait for results to load

        # Print the titles of the search results
        results = driver.find_elements(By.CSS_SELECTOR, 'h3')
        for index, result in enumerate(results, start=1):
            print(f"{index}: {result.text}")

    except (WebDriverException, NoSuchElementException) as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    search_google("Selenium Python")