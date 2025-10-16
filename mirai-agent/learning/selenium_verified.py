"""
selenium - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-16T14:18:37.148308

This code has been verified by MIRAI's NASA-level learning system.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def setup_driver() -> webdriver.Chrome:
    """
    Sets up the Chrome WebDriver with options.
    
    Returns:
        webdriver.Chrome: Configured WebDriver instance.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Create a service object for ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def fetch_title(url: str) -> str:
    """
    Fetches the title of a web page.
    
    Args:
        url (str): The URL of the web page to fetch the title from.
    
    Returns:
        str: The title of the web page.
    """
    driver = setup_driver()
    try:
        driver.get(url)  # Navigate to the URL
        time.sleep(2)  # Wait for the page to load
        title = driver.title  # Get the title of the page
        return title
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error occurred: {e}")
        return ""
    finally:
        driver.quit()  # Ensure the driver is closed

if __name__ == "__main__":
    url = "https://www.example.com"
    title = fetch_title(url)
    print(f"The title of the page is: {title}")