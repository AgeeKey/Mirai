"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-15T10:39:11.525813

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to send the request to.
        params (Optional[Dict[str, Any]]): Optional query parameters to include in the request.

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the server, or None if an error occurred.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url, params=params)
        
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Parse and return the JSON response
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Handle other request-related errors
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Handle JSON decoding errors

    return None

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"
    params = {'key': 'value'}
    
    data = fetch_data(url, params)
    if data is not None:
        print(data)  # Print the fetched data