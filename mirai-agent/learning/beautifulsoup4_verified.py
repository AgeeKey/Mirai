"""
beautifulsoup4 - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 0/1
Learned: 2025-10-15T23:56:13.375016

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

def fetch_html(url: str) -> Optional[str]:
    """
    Fetch the HTML content of a given URL.

    :param url: The URL of the webpage to fetch.
    :return: The HTML content as a string, or None if an error occurs.
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
    Parse the HTML content and extract all the hyperlinks.

    :param html: The HTML content to parse.
    :return: A list of hyperlinks found in the HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    # Find all anchor tags and extract the href attribute
    for anchor in soup.find_all('a', href=True):
        links.append(anchor['href'])

    return links

def main(url: str) -> None:
    """
    Main function to fetch and parse HTML from a URL.

    :param url: The URL of the webpage to scrape.
    """
    html = fetch_html(url)
    if html:
        links = parse_html(html)
        print("Found links:")
        for link in links:
            print(link)

if __name__ == "__main__":
    target_url = "https://example.com"  # Replace with the desired URL
    main(target_url)