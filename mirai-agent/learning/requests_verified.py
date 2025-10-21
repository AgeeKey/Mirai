"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 1/1
Learned: 2025-10-21T16:30:42.068183

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetches data from the specified URL using an HTTP GET request.

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
        raise ValueError("Invalid URL provided. Please ensure it starts with 'http' or 'https'.")

    try:
        response = requests.get(url)  # Send GET request to the URL
        response.raise_for_status()  # Raise an error for bad responses (4XX and 5XX)
        return response.json()  # Return the JSON response as a dictionary
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")  # Log request errors
        raise

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Example URL
    try:
        data = fetch_data(url)  # Fetch data from the URL
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any errors