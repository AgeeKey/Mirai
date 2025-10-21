"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-21T03:23:52.657942

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data(url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch data from a given URL with optional query parameters.

    :param url: The URL to send the GET request to.
    :param params: Optional dictionary of query parameters to include in the request.
    :return: Parsed JSON response as a dictionary.
    :raises HTTPError: If the HTTP request returned an unsuccessful status code.
    :raises RequestException: For other request-related errors.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        
        # Return the JSON response as a dictionary
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log the HTTP error
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log the request error
        raise

# Example usage
if __name__ == "__main__":
    api_url = "https://api.example.com/data"
    query_params = {"key": "value"}
    
    try:
        data = fetch_data(api_url, params=query_params)
        print(data)  # Output the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")