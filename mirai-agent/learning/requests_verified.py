"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.92
Tests Passed: 1/1
Learned: 2025-10-18T07:55:31.375939

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetches data from a given URL using an HTTP GET request.

    Args:
        url (str): The URL to send the request to.
        params (Optional[dict]): Optional dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not JSON or is empty.
        HTTPError: If an HTTP error occurs.
        RequestException: For other request-related errors.
    """
    try:
        # Send a GET request to the specified URL
        response = requests.get(url, params=params)
        
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        
        # Attempt to return the response as JSON
        return response.json()
    
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Log HTTP errors
        raise
    except RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Log other request errors
        raise
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")  # Log JSON errors
        raise ValueError("Response content is not valid JSON or is empty.")

if __name__ == "__main__":
    # Example URL for testing
    test_url = "https://jsonplaceholder.typicode.com/posts"
    try:
        # Fetch data from the example URL
        data = fetch_data(test_url)
        print(data)  # Print the fetched data
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any exceptions during data fetching