"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 1/1
Learned: 2025-10-14T15:15:44.533805

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (Dict[str, Any], optional): Query parameters to include in the request.

    Returns:
        Dict[str, Any]: The JSON response data.

    Raises:
        ValueError: If the URL is invalid.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related issues.
    """
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL: Must start with 'http://' or 'https://'")

    try:
        # Send a GET request to the specified URL
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        
        # Return the JSON response data
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        raise

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"
    query_params = {"key": "value", "page": 1}
    
    try:
        data = fetch_data(url, params=query_params)
        print(data)
    except (ValueError, HTTPError, RequestException) as e:
        print(f"An error occurred: {e}")