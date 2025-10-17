"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.90
Tests Passed: 1/1
Learned: 2025-10-17T05:56:52.345003

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to which the request is sent.
        params (Optional[dict]): Optional dictionary of query parameters.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not JSON.
        RequestException: For other request-related errors.
    """
    try:
        # Send a GET request
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Return the JSON response
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except ValueError as json_err:
        print(f"Error parsing JSON: {json_err}")
        raise ValueError("Response content is not valid JSON.")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        raise

# Example usage
if __name__ == "__main__":
    url = "https://api.example.com/data"
    params = {"key": "value"}
    
    try:
        data = fetch_data(url, params)
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")