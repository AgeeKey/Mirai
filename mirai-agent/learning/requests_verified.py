"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-16T05:48:28.281610

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from the specified URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict[str, Any]: The JSON response data as a dictionary.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If an HTTP error occurs during the request.
        RequestException: For other request-related errors.
    """
    if not url.startswith('http'):
        raise ValueError("Invalid URL provided")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response as a dictionary
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log other request errors
        raise

# Example usage
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts/1"
    try:
        data = fetch_data(url)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle the error