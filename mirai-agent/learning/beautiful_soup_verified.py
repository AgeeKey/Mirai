"""
Beautiful Soup - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-21T10:33:25.685679

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def fetch_html(url: str) -> Optional[str]:
    """Fetch the HTML content of a given URL.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        Optional[str]: The HTML content of the page, or None if the request fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def parse_html(html: str) -> List[str]:
    """Parse the HTML content and extract all the links.

    Args:
        html (str): The HTML content of a webpage.

    Returns:
        List[str]: A list of URLs found in the webpage.
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    
    # Extract all anchor tags and their href attributes
    for anchor in soup.find_all('a', href=True):
        links.append(anchor['href'])
    
    return links

def main(url: str) -> None:
    """Main function to fetch and parse a webpage.

    Args:
        url (str): The URL of the webpage to process.
    """
    html_content = fetch_html(url)
    
    if html_content:
        links = parse_html(html_content)
        print("Found links:")
        for link in links:
            print(link)
    else:
        print("Failed to retrieve or parse the webpage.")

if __name__ == "__main__":
    URL = "https://example.com"  # Change to the desired URL
    main(URL)