"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 1/1
Learned: 2025-10-21T12:42:47.818338

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> Optional[dict]:
    """
    Fetch data from the given URL with optional parameters.

    Args:
        url (str): The URL to fetch data from.
        params (Optional[dict]): A dictionary of query parameters to include in the request.

    Returns:
        Optional[dict]: The JSON response data if the request is successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url, params=params)
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the JSON response as a dictionary
        return response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Print any request error
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Print JSON decode error
    return None

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://jsonplaceholder.typicode.com/todos/1"
    data = fetch_data(url)
    if data:
        print(data)  # Print the fetched data