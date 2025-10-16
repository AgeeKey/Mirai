"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 1/1
Learned: 2025-10-16T15:08:05.114805

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetches data from a given URL with optional query parameters.

    Args:
        url (str): The URL to fetch data from.
        params (Optional[Dict[str, Any]]): Optional dictionary of query parameters.

    Returns:
        Optional[Dict[str, Any]]: The JSON response if successful, None otherwise.
    """
    try:
        response = requests.get(url, params=params)  # Make the GET request
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Return the JSON response if successful
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")  # Handle other request errors
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Handle JSON decoding errors
    return None  # Return None if an error occurred

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid URL
    parameters = {"key": "value"}  # Replace with actual query parameters
    result = fetch_data(url, parameters)  # Fetch data from the URL
    if result is not None:
        print(result)  # Print the fetched data