"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-20T13:13:59.776091

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from the specified URL.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related errors.
    """
    if not url.startswith("http"):
        raise ValueError("Invalid URL provided. Must start with 'http' or 'https'.")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        return response.json()  # Return the response as JSON
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        raise

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid URL
    try:
        data = fetch_data(url)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")