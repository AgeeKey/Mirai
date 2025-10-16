"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 1/1
Learned: 2025-10-16T05:15:55.620162

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str) -> Optional[dict]:
    """
    Fetches data from the specified URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Optional[dict]: The JSON response if the request is successful, None otherwise.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Raise an exception for HTTP errors
        response.raise_for_status()
        # Return the JSON response as a dictionary
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Print general request error
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Print JSON decoding error
    return None

if __name__ == "__main__":
    # Example usage
    url = "https://api.github.com/repos/psf/requests"
    data = fetch_data(url)
    if data:
        print(data)  # Print the fetched data