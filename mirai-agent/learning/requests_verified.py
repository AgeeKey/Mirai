"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-21T14:04:06.605207

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict

def fetch_data(url: str, params: Optional[Dict[str, str]] = None) -> Optional[dict]:
    """
    Fetch data from a given URL using a GET request.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, str]]): Optional query parameters for the request.

    Returns:
        Optional[dict]: The JSON response as a dictionary, or None if an error occurred.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url, params=params)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Return the JSON response
        return response.json()
        
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log request errors
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Log JSON decoding errors
    return None

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.example.com/data"
    parameters = {"key": "value"}
    
    data = fetch_data(url, params=parameters)
    if data is not None:
        print(data)