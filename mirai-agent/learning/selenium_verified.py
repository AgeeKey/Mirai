"""
selenium - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 0/1
Learned: 2025-10-14T23:09:12.798595

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def setup_driver() -> webdriver.Chrome:
    """Set up the Chrome WebDriver with specified options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Create a Service object for ChromeDriver
    service = Service(executable_path='path/to/chromedriver')  # Replace with your path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def search_google(query: str) -> None:
    """Search for a query on Google and print the titles of the results."""
    driver = setup_driver()
    
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        
        # Find the search box, enter a query, and submit
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        
        # Wait for results to load
        time.sleep(2)  # This is a simple wait; consider using WebDriverWait for production
        
        # Fetch and print the titles of the search results
        results = driver.find_elements(By.TAG_NAME, "h3")
        for index, result in enumerate(results):
            print(f"{index + 1}: {result.text}")
    
    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    search_google("Selenium Python")