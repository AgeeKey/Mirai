"""
requests - Verified Learning Artifact

Quality Grade: A
Overall Score: 0.98
Tests Passed: 1/1
Learned: 2025-10-15T19:19:41.754912

This code has been verified by MIRAI's NASA-level learning system.
"""

import requests
from requests.exceptions import HTTPError, RequestException
from typing import Optional

def fetch_data(url: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from a specified URL using HTTP GET request.

    Args:
        url (str): The URL to send the request to.
        params (Optional[dict]): Optional dictionary of query parameters to include in the request.

    Returns:
        dict: The JSON response from the server.

    Raises:
        ValueError: If the response is not in JSON format.
        HTTPError: For HTTP errors encountered during the request.
        RequestException: For other request-related errors.
    """
    try:
        # Sending GET request to the specified URL
        response = requests.get(url, params=params)
        # Raise an error for bad responses (4xx and 5xx)
        response.raise_for_status()
        # Attempt to return the JSON response
        return response.json()
    except ValueError as ve:
        # Handle cases where response is not JSON
        raise ValueError("Response content is not valid JSON") from ve
    except HTTPError as http_err:
        # Handle HTTP errors
        raise HTTPError(f"HTTP error occurred: {http_err}") from http_err
    except RequestException as req_err:
        # Handle other request-related exceptions
        raise RequestException(f"An error occurred: {req_err}") from req_err

if __name__ == "__main__":
    try:
        # Example URL to fetch data from
        example_url = "https://jsonplaceholder.typicode.com/posts"
        # Fetching data with optional parameters
        data = fetch_data(example_url, params={"userId": 1})
        print(data)
    except Exception as e:
        print(f"An error occurred: {e}")