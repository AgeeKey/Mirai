"""
requests - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.90
Tests Passed: 1/1
Learned: 2025-10-17T03:17:19.186394

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from a given URL using a GET request.

    Args:
        url (str): The URL to send the GET request to.
        params (Optional[dict]): A dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not in JSON format.
        HTTPError: If the HTTP request returned an unsuccessful status code.
        RequestException: For other request-related errors.
    """
    try:
        # Sending GET request to the provided URL
        response = requests.get(url, params=params)
        
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        
        # Attempt to return JSON data
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except ValueError as json_err:
        print(f"Value error occurred: {json_err}")  # Log JSON parsing errors
        raise ValueError("Response content is not in JSON format.")
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log any other request errors
        raise

# Example usage
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"userId": 1}
    
    try:
        data = fetch_data(url, params)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle errors gracefully