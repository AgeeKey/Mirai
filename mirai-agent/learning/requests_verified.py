"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.93
Tests Passed: 1/1
Learned: 2025-10-19T17:12:28.966423

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Dict, Any

def fetch_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from a given URL using an HTTP GET request.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        ValueError: If the response is not JSON.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For any other request-related errors.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Attempt to return the JSON response
        return response.json()
    except ValueError as ve:
        print("Error decoding JSON:", ve)
        raise
    except HTTPError as http_err:
        print("HTTP error occurred:", http_err)
        raise
    except RequestException as req_err:
        print("Error during request:", req_err)
        raise

if __name__ == "__main__":
    # Example URL for testing
    api_url = "https://jsonplaceholder.typicode.com/posts/1"
    
    try:
        # Fetch data from the API
        data = fetch_data(api_url)
        print("Fetched Data:", data)
    except Exception as e:
        print("An error occurred:", e)