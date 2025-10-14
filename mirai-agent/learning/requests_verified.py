"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 1/1
Learned: 2025-10-14T21:31:28.358289

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a specified URL with optional query parameters.

    Args:
        url (str): The URL to make the request to.
        params (Optional[Dict[str, Any]]): Optional dictionary of query parameters to include in the request.

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the server, or None if an error occurs.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Return the JSON content of the response
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Handle other request-related errors
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Handle JSON decoding errors
    return None  # Return None if an error occurred

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with an actual API endpoint
    params = {'key': 'value'}  # Example query parameters
    data = fetch_data(url, params)
    if data:
        print("Fetched data:", data)
    else:
        print("Failed to fetch data.")