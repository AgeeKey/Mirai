"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 1/1
Learned: 2025-10-22T03:02:26.304778

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException
from typing import Any, Dict, Optional

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetches data from the given URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[Dict[str, Any]]): A dictionary of query parameters to include in the request.

    Returns:
        Optional[Dict[str, Any]]: The JSON response as a dictionary if the request was successful, None otherwise.
    """
    try:
        response = requests.get(url, params=params)  # Send GET request
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        return response.json()  # Return the response JSON as a dictionary

    except RequestException as e:
        print(f"An error occurred: {e}")  # Print error message
        return None  # Return None if there was an error

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Example URL
    params = {"key": "value"}  # Example query parameters
    data = fetch_data(url, params)  # Fetch data from the API

    if data is not None:
        print(data)  # Print the fetched data
    else:
        print("Failed to fetch data.")  # Print failure message