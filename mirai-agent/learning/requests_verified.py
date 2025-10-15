"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-15T06:19:46.365820

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str) -> Optional[dict]:
    """
    Fetch data from a given URL and return it as a dictionary.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Optional[dict]: The JSON response as a dictionary if successful, None otherwise.
    """
    try:
        response = requests.get(url)  # Send a GET request to the specified URL
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        return response.json()  # Parse the JSON response and return it as a dictionary

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print HTTP error message
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")  # Print request error message
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Print JSON decoding error message

    return None  # Return None if there was an error

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Replace with a valid API endpoint
    data = fetch_data(url)  # Fetch data from the API

    if data:
        print(data)  # Print the fetched data
    else:
        print("Failed to retrieve data.")  # Notify failure to retrieve data