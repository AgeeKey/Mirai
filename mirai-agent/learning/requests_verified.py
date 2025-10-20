"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-20T06:36:33.583215

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from a specified URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[dict]): A dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related errors.
    """
    if not url.startswith('http'):
        raise ValueError("Invalid URL: Must start with 'http' or 'https'.")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response as a dictionary
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log other request errors
        raise

if __name__ == "__main__":
    url = "https://api.example.com/data"
    query_params = {"key": "value"}
    
    try:
        data = fetch_data(url, params=query_params)
        print("Fetched data:", data)
    except Exception as e:
        print("An error occurred:", e)