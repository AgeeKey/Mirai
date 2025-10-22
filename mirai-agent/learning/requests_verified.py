"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 1/1
Learned: 2025-10-22T05:09:19.909004

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str) -> Optional[dict]:
    """
    Fetch data from the specified URL using a GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Optional[dict]: The JSON response as a dictionary if successful, None otherwise.
    """
    try:
        # Sending the GET request
        response = requests.get(url)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Return the JSON response as a dictionary
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
    except RequestException as req_err:
        print(f"Error occurred during the request: {req_err}")  # Log request errors
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Log JSON decoding errors
    return None

if __name__ == "__main__":
    # Example usage
    url = "https://api.github.com/repos/psf/requests"
    data = fetch_data(url)
    if data:
        print(data)