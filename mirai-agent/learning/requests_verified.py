"""
Requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.97
Tests Passed: 1/1
Learned: 2025-10-19T21:55:55.852173

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Any, Dict, Optional

def fetch_data(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to fetch data from.
        params (Optional[Dict[str, Any]]): Optional dictionary of query parameters.

    Returns:
        Optional[Dict[str, Any]]: Parsed JSON response if successful, None otherwise.
    """
    try:
        # Sending a GET request to the specified URL
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP errors (4xx and 5xx responses)
        response.raise_for_status()
        
        # Return the JSON response as a dictionary
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")
    
    return None

if __name__ == "__main__":
    # Example usage of the fetch_data function
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1}
    
    # Fetch data from the API
    data = fetch_data(url, params)
    
    # Print the fetched data if available
    if data:
        print(data)