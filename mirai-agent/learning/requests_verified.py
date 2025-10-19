"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.96
Tests Passed: 1/1
Learned: 2025-10-19T18:15:21.334809

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str) -> Optional[dict]:
    """Fetch data from a given URL and return it as a dictionary.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Optional[dict]: The JSON response as a dictionary if successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Return the JSON content as a dictionary
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Specific HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # General request error
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # JSON decoding error
    return None

if __name__ == "__main__":
    # Example URL to fetch data from
    example_url = "https://api.github.com/repos/psf/requests"
    
    # Fetch data and print the result
    data = fetch_data(example_url)
    if data:
        print(data)