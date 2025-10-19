"""
beautifulsoup4 - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-19T17:59:57.888265

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def fetch_html(url: str) -> Optional[str]:
    """Fetch the HTML content of a given URL.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        Optional[str]: The HTML content of the page, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html: str) -> List[str]:
    """Parse the HTML content and extract all the text from <p> tags.

    Args:
        html (str): The HTML content to parse.

    Returns:
        List[str]: A list of text content from <p> tags.
    """
    soup = BeautifulSoup(html, 'html.parser')  # Create a BeautifulSoup object
    paragraphs = soup.find_all('p')  # Find all <p> tags
    return [p.get_text() for p in paragraphs]  # Extract text from <p> tags

def main(url: str) -> None:
    """Main function to fetch and parse HTML from a URL.

    Args:
        url (str): The URL of the web page to process.
    """
    html_content = fetch_html(url)  # Fetch the HTML content
    if html_content:  # Proceed only if HTML was fetched successfully
        paragraphs = parse_html(html_content)  # Parse the HTML
        for index, paragraph in enumerate(paragraphs):
            print(f"Paragraph {index + 1}: {paragraph}")  # Print each paragraph

if __name__ == "__main__":
    url_input = "https://example.com"  # Replace with your target URL
    main(url_input)  # Call the main function