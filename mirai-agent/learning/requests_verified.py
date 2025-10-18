"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.83
Tests Passed: 1/1
Learned: 2025-10-18T05:17:34.908771

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data_from_api(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch data from a specified API endpoint.

    Args:
        url (str): The URL of the API endpoint.
        params (Dict[str, Any], optional): Query parameters to include in the request.

    Returns:
        Dict[str, Any]: The JSON response from the API.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For general request exceptions.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("Invalid URL provided.")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()  # Return the JSON response

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")  # Log request exceptions
        raise

# Example usage
if __name__ == "__main__":
    api_url = "https://api.example.com/data"
    query_parameters = {"key": "value"}
    
    try:
        data = fetch_data_from_api(api_url, query_parameters)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions during the fetch