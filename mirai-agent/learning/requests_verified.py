"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.84
Tests Passed: 1/1
Learned: 2025-10-17T12:23:29.615765

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Any, Dict

def fetch_data(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch data from the specified URL with optional query parameters.

    Args:
        url (str): The URL to make the GET request to.
        params (Dict[str, Any], optional): A dictionary of query parameters to include in the request.

    Returns:
        Dict[str, Any]: The JSON response data from the server.

    Raises:
        ValueError: If the response is not JSON.
        HTTPError: If an HTTP error occurs during the request.
        Timeout: If the request times out.
        RequestException: For any other request-related error.
    """
    try:
        response = requests.get(url, params=params, timeout=10)  # Set a timeout of 10 seconds
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")  # Log timeout errors
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log other request-related errors
        raise
    except ValueError as json_err:
        print(f"JSON decoding failed: {json_err}")  # Log JSON decoding errors
        raise

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"
    params = {"key": "value"}
    
    try:
        data = fetch_data(url, params)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions raised during the fetch