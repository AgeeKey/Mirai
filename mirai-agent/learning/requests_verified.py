"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.99
Tests Passed: 1/1
Learned: 2025-10-14T21:15:12.150986

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
        params (Optional[Dict[str, Any]]): Query parameters to include in the request.

    Returns:
        Optional[Dict[str, Any]]: The JSON response if the request is successful, None otherwise.
    """
    try:
        # Send a GET request to the specified URL with optional parameters
        response = requests.get(url, params=params)
        # Raise an exception for HTTP errors
        response.raise_for_status()
        # Return the JSON response if successful
        return response.json()
    except RequestException as e:
        # Print the error message for debugging
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1}
    
    data = fetch_data(url, params)
    if data:
        # Print the fetched data
        print(data)