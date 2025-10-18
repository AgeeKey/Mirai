"""
beautifulsoup4 - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-18T05:17:49.823469

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def fetch_html(url: str) -> Optional[str]:
    """Fetches HTML content from a given URL.

    Args:
        url (str): The URL to fetch the HTML from.

    Returns:
        Optional[str]: The HTML content if the request is successful, None otherwise.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html: str) -> List[str]:
    """Parses HTML content and extracts all the text from paragraph tags.

    Args:
        html (str): The HTML content to parse.

    Returns:
        List[str]: A list of text from each paragraph tag.
    """
    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML
    paragraphs = soup.find_all('p')  # Find all paragraph tags
    return [p.get_text() for p in paragraphs]  # Extract text from each paragraph

def main(url: str) -> None:
    """Main function to fetch and parse HTML content from a given URL.

    Args:
        url (str): The URL to fetch and parse.
    """
    html_content = fetch_html(url)  # Fetch HTML content
    if html_content:  # Check if content was fetched successfully
        paragraphs = parse_html(html_content)  # Parse the HTML
        for i, paragraph in enumerate(paragraphs, start=1):
            print(f"Paragraph {i}: {paragraph}")  # Print each paragraph

if __name__ == "__main__":
    url_to_scrape = 'https://example.com'  # Replace with the desired URL
    main(url_to_scrape)  # Execute the main function