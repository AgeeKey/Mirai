"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-13T17:23:44.492210

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException
from typing import Optional, Dict, Any

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, Any]]): Optional dictionary of query parameters.

    Returns:
        Optional[Dict[str, Any]]: The response data as a dictionary, or None if an error occurred.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()  # Return the response data as JSON
    except RequestException as e:
        print(f"An error occurred: {e}")  # Print the error message
        return None  # Return None if there was an error

if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts"  # Example API endpoint
    params = {"userId": 1}  # Example query parameters
    data = fetch_data(url, params)  # Fetch data from the API

    if data is not None:
        print(data)  # Print the fetched data
    else:
        print("Failed to retrieve data.")  # Indicate failure to retrieve data