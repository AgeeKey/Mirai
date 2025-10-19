"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 1/1
Learned: 2025-10-19T06:56:30.463946

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from the specified URL using an HTTP GET request.

    Args:
        url (str): The URL to send the request to.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        RuntimeError: If an error occurs during the request.
    """
    if not url.startswith('http'):
        raise ValueError("Invalid URL provided. Must start with 'http'.")

    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an exception for HTTP errors (4xx and 5xx responses)
        response.raise_for_status()
        
        # Return the JSON response
        return response.json()

    except HTTPError as http_err:
        raise RuntimeError(f"HTTP error occurred: {http_err}") from http_err
    except RequestException as req_err:
        raise RuntimeError(f"Request exception occurred: {req_err}") from req_err

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid API endpoint
    try:
        data = fetch_data(url)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")