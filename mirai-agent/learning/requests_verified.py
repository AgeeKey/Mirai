"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-19T19:34:16.306356

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> Optional[dict]:
    """
    Fetch data from a given URL using a GET request.

    Args:
        url (str): The URL to fetch data from.
        params (Optional[dict]): Optional dictionary of query parameters.

    Returns:
        Optional[dict]: The JSON response if the request was successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL with optional parameters
        response = requests.get(url, params=params)

        # Raise an exception for HTTP error responses (4xx and 5xx)
        response.raise_for_status()

        # Return the JSON response if the request was successful
        return response.json()

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Print general request error
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Print JSON decoding error

    return None  # Return None if an error occurred

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.example.com/data"
    params = {"key": "value"}
    data = fetch_data(url, params)
    
    if data:
        print(data)  # Print the fetched data
    else:
        print("Failed to retrieve data.")