"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 1/1
Learned: 2025-10-16T23:31:01.609527

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from a specified URL using an HTTP GET request.

    Args:
        url (str): The URL from which to fetch data.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For any other request-related errors.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("Invalid URL. Must start with 'http://' or 'https://'.")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Return the parsed JSON response
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP error
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log request error
        raise

if __name__ == "__main__":
    url = "https://api.github.com/repos/psf/requests"  # Example URL
    try:
        data = fetch_data(url)  # Fetching data from the URL
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Log any other exceptions