"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-21T21:23:56.297733

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from the specified URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[dict]): Optional dictionary of query parameters.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not JSON or cannot be decoded.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related errors.
    """
    try:
        response = requests.get(url, params=params)  # Send GET request
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return JSON response as a dictionary
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP error
        raise
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Log JSON decode error
        raise ValueError("Response content is not valid JSON.")
    except RequestException as req_err:
        print(f"Request error: {req_err}")  # Log request error
        raise

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid API endpoint
    params = {"key": "value"}  # Example query parameters

    try:
        data = fetch_data(url, params)  # Fetch data from the API
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any errors that occur