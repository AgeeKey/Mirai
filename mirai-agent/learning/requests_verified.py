"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-16T18:06:58.021081

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict

def fetch_data(url: str, params: Dict[str, Any] = None) -> Any:
    """
    Fetch data from a given URL with optional query parameters.

    :param url: The URL to fetch data from.
    :param params: Optional dictionary of query parameters to include in the request.
    :return: The JSON response from the server, or None if an error occurs.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        
        # Return the JSON content of the response
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP error
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log request error
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")  # Log JSON decode error
    
    return None  # Return None if an error occurred

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://api.example.com/data"
    params = {"key": "value"}
    
    result = fetch_data(url, params)
    
    if result is not None:
        print("Data fetched successfully:", result)
    else:
        print("Failed to fetch data.")