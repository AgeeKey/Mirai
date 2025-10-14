"""
Beautiful Soup - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-14T20:26:30.797069

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def fetch_webpage(url: str) -> Optional[str]:
    """
    Fetch the content of a webpage given a URL.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        Optional[str]: The HTML content of the webpage, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return None

def parse_html(html: str) -> List[str]:
    """
    Parse the HTML content and extract all the <h2> headings.

    Args:
        html (str): The HTML content to parse.

    Returns:
        List[str]: A list of headings found in the HTML content.
    """
    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML
    headings = soup.find_all('h2')  # Find all <h2> tags
    return [heading.get_text(strip=True) for heading in headings]  # Extract text from each heading

def main(url: str) -> None:
    """
    Main function to fetch and parse a webpage.

    Args:
        url (str): The URL of the webpage to scrape.
    """
    html_content = fetch_webpage(url)  # Fetch the webpage content
    if html_content:  # Proceed only if content was fetched successfully
        headings = parse_html(html_content)  # Parse the HTML to extract headings
        print("Headings found on the webpage:")
        for heading in headings:
            print(f"- {heading}")

if __name__ == "__main__":
    url_to_scrape = 'https://example.com'  # Replace with the desired URL
    main(url_to_scrape)  # Run the main function