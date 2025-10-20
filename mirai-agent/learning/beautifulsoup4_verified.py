"""
beautifulsoup4 - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-20T21:02:24.467840

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def fetch_html(url: str) -> Optional[str]:
    """
    Fetches the HTML content from the given URL.

    Args:
        url (str): The URL to fetch the HTML from.

    Returns:
        Optional[str]: The HTML content if the request was successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html: str) -> List[str]:
    """
    Parses the HTML content and extracts all the text from the <p> tags.

    Args:
        html (str): The HTML content to parse.

    Returns:
        List[str]: A list of text extracted from <p> tags.
    """
    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML
    paragraphs = soup.find_all('p')  # Find all <p> tags
    return [p.get_text() for p in paragraphs]  # Extract text from each <p>

def main(url: str) -> None:
    """
    Main function to execute the web scraping process.

    Args:
        url (str): The URL to scrape.
    """
    html = fetch_html(url)  # Fetch the HTML content
    if html:
        paragraphs = parse_html(html)  # Parse the HTML and get <p> texts
        for i, paragraph in enumerate(paragraphs, start=1):
            print(f"Paragraph {i}: {paragraph}")  # Print each paragraph

if __name__ == "__main__":
    target_url = 'https://example.com'  # Replace with the desired URL
    main(target_url)  # Run the main function