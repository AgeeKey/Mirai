"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 1/1
Learned: 2025-10-18T02:07:35.881257

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, Timeout, RequestException

def fetch_data(url: str, params: dict = None) -> dict:
    """
    Fetch data from a given URL with optional query parameters.

    Args:
        url (str): The URL to send the GET request to.
        params (dict, optional): A dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response content is not JSON.
        HTTPError: If an HTTP error occurs.
        Timeout: If the request times out.
        RequestException: For other request-related errors.
    """
    try:
        # Send a GET request to the specified URL with optional parameters
        response = requests.get(url, params=params, timeout=10)
        
        # Raise an exception for HTTP errors (4xx and 5xx responses)
        response.raise_for_status()
        
        # Attempt to parse the response as JSON
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        raise
    except ValueError as json_err:
        print(f"Error parsing JSON response: {json_err}")
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