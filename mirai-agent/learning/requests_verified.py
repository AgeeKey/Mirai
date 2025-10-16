"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.82
Tests Passed: 1/1
Learned: 2025-10-16T17:17:51.609434

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import RequestException
from typing import Dict, Any

def fetch_data(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetches data from the specified URL with optional query parameters.

    Args:
        url (str): The URL to fetch data from.
        params (Dict[str, Any], optional): A dictionary of query parameters to include in the request.

    Returns:
        Dict[str, Any]: The JSON response data from the server.

    Raises:
        RequestException: An error occurred while making the request.
    """
    try:
        response = requests.get(url, params=params)  # Send a GET request
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the JSON response
    except RequestException as e:
        print(f"An error occurred: {e}")  # Print the error message
        raise  # Re-raise the exception for further handling

if __name__ == "__main__":
    url = "https://api.example.com/data"  # Example API endpoint
    query_params = {"key": "value"}  # Example query parameters

    try:
        data = fetch_data(url, query_params)  # Fetch data from the API
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"Failed to fetch data: {e}")  # Handle any exceptions