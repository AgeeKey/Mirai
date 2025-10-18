"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.91
Tests Passed: 1/1
Learned: 2025-10-18T18:05:46.356331

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any, Optional

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Fetch data from a specified URL with optional query parameters.

    Args:
        url (str): The URL to fetch data from.
        params (Optional[Dict[str, Any]]): Optional query parameters to include in the request.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For any other request-related errors.
    """
    try:
        # Send a GET request to the provided URL with query parameters
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Return the JSON response if successful
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log the HTTP error
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log the request error
        raise

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.example.com/data"
    query_params = {"key": "value"}

    try:
        result = fetch_data(url, params=query_params)
        print(result)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions